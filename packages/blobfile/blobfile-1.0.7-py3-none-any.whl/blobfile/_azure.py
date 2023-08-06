import urllib.parse
import os
import json
import hmac
import base64
import datetime
import time
import calendar
import re
from typing import Any, Mapping, Dict, Tuple, Sequence, List

import xmltodict

from blobfile import _common as common
from blobfile._common import Request, Error

SHARED_KEY = "shared_key"
OAUTH_TOKEN = "oauth_token"
ANONYMOUS = "anonymous"


def load_credentials() -> Dict[str, Any]:
    # https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/identity/azure-identity#environment-variables
    # AZURE_STORAGE_KEY seems to be the environment variable mentioned by the az cli
    # AZURE_STORAGE_ACCOUNT_KEY is mentioned elsewhere on the internet
    for varname in ["AZURE_STORAGE_KEY", "AZURE_STORAGE_ACCOUNT_KEY"]:
        if varname in os.environ:
            result = dict(storageAccountKey=os.environ[varname])
            if "AZURE_STORAGE_ACCOUNT" in os.environ:
                result["account"] = os.environ["AZURE_STORAGE_ACCOUNT"]
            return result

    if "AZURE_APPLICATION_CREDENTIALS" in os.environ:
        creds_path = os.environ["AZURE_APPLICATION_CREDENTIALS"]
        if not os.path.exists(creds_path):
            raise Error(
                f"Credentials not found at '{creds_path}' specified by environment variable 'AZURE_APPLICATION_CREDENTIALS'"
            )
        with open(creds_path) as f:
            return json.load(f)

    if "AZURE_CLIENT_ID" in os.environ:
        return dict(
            appId=os.environ["AZURE_CLIENT_ID"],
            password=os.environ["AZURE_CLIENT_SECRET"],
            tenant=os.environ["AZURE_TENANT_ID"],
        )

    if "AZURE_STORAGE_CONNECTION_STRING" in os.environ:
        connection_data = {}
        # technically this should be parsed according to the rules in https://www.connectionstrings.com/formating-rules-for-connection-strings/
        for part in os.environ["AZURE_STORAGE_CONNECTION_STRING"].split(";"):
            key, _, val = part.partition("=")
            connection_data[key.lower()] = val
        return dict(
            account=connection_data["accountname"],
            storageAccountKey=connection_data["accountkey"],
        )

    # look for a refresh token in the az command line credentials
    # https://mikhail.io/2019/07/how-azure-cli-manages-access-tokens/
    default_creds_path = os.path.expanduser("~/.azure/accessTokens.json")
    if os.path.exists(default_creds_path):
        with open(default_creds_path) as f:
            tokens = json.load(f)
            best_token = None
            for token in tokens:
                if best_token is None:
                    best_token = token
                else:
                    # expiresOn may be missing for tokens from service principals
                    if token.get("expiresOn", "") > best_token.get("expiresOn", ""):
                        best_token = token
            if best_token is not None:
                return best_token

    return {}


def load_subscription_ids() -> List[str]:
    """
    Return a list of subscription ids from the local azure profile
    the default subscription will appear first in the list
    """
    default_profile_path = os.path.expanduser("~/.azure/azureProfile.json")
    if not os.path.exists(default_profile_path):
        return []

    with open(default_profile_path, "rb") as f:
        # this file has a UTF-8 BOM
        profile = json.loads(f.read().decode("utf-8-sig"))
    subscriptions = profile["subscriptions"]

    def key_fn(x: Mapping[str, Any]) -> bool:
        return x["isDefault"]

    subscriptions.sort(key=key_fn, reverse=True)
    return [sub["id"] for sub in subscriptions]


def build_url(account: str, template: str, **data: str) -> str:
    return common.build_url(
        f"https://{account}.blob.core.windows.net", template, **data
    )


def create_access_token_request(
    creds: Mapping[str, str], scope: str, success_codes: Sequence[int] = (200,)
) -> Request:
    if "refreshToken" in creds:
        # https://docs.microsoft.com/en-us/azure/active-directory/develop/v1-protocols-oauth-code#refreshing-the-access-tokens
        data = {
            "grant_type": "refresh_token",
            "refresh_token": creds["refreshToken"],
            "resource": scope,
        }
        tenant = "common"
    else:
        # https://docs.microsoft.com/en-us/azure/active-directory/develop/v1-oauth2-client-creds-grant-flow#request-an-access-token
        # https://docs.microsoft.com/en-us/azure/active-directory/develop/v1-protocols-oauth-code
        # https://docs.microsoft.com/en-us/rest/api/storageservices/authorize-with-azure-active-directory#use-oauth-access-tokens-for-authentication
        # https://docs.microsoft.com/en-us/rest/api/azure/
        # https://docs.microsoft.com/en-us/rest/api/storageservices/authorize-with-azure-active-directory
        # az ad sp create-for-rbac --name <name>
        # az account list
        # az role assignment create --role "Storage Blob Data Contributor" --assignee <appid> --scope "/subscriptions/<account id>"
        data = {
            "grant_type": "client_credentials",
            "client_id": creds["appId"],
            "client_secret": creds["password"],
            "resource": scope,
        }
        tenant = creds["tenant"]
    return Request(
        url=f"https://login.microsoftonline.com/{tenant}/oauth2/token",
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=urllib.parse.urlencode(data).encode("utf8"),
        success_codes=success_codes,
    )


def create_user_delegation_sas_request(account: str) -> Request:
    # https://docs.microsoft.com/en-us/rest/api/storageservices/create-user-delegation-sas
    now = datetime.datetime.utcnow()
    start = (now + datetime.timedelta(hours=-1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    expiration = now + datetime.timedelta(days=6)
    expiry = expiration.strftime("%Y-%m-%dT%H:%M:%SZ")
    return Request(
        url=f"https://{account}.blob.core.windows.net/",
        method="POST",
        params=dict(restype="service", comp="userdelegationkey"),
        data={"KeyInfo": {"Start": start, "Expiry": expiry}},
    )


def make_api_request(req: Request, auth: Tuple[str, str]) -> Request:
    if req.headers is None:
        headers = {}
    else:
        headers = dict(req.headers).copy()

    if req.params is None:
        params = {}
    else:
        params = dict(req.params).copy()

    # https://docs.microsoft.com/en-us/rest/api/storageservices/previous-azure-storage-service-versions
    headers["x-ms-version"] = "2019-02-02"
    headers["x-ms-date"] = datetime.datetime.utcnow().strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )
    data = req.data
    if data is not None and isinstance(data, dict):
        data = xmltodict.unparse(data).encode("utf8")

    result = Request(
        method=req.method,
        url=req.url,
        params=params,
        headers=headers,
        data=data,
        preload_content=req.preload_content,
        success_codes=tuple(req.success_codes),
        retry_codes=tuple(req.retry_codes),
    )

    kind, token = auth
    if kind == SHARED_KEY:
        # make sure we are signing the request that has the ms headers added already
        headers["Authorization"] = sign_with_shared_key(result, token)
    elif kind == OAUTH_TOKEN:
        headers["Authorization"] = f"Bearer {token}"
    elif kind == ANONYMOUS:
        pass
    return result


def generate_signed_url(key: Mapping[str, str], url: str) -> Tuple[str, float]:
    # https://docs.microsoft.com/en-us/rest/api/storageservices/delegate-access-with-shared-access-signature
    # https://docs.microsoft.com/en-us/rest/api/storageservices/create-user-delegation-sas
    # https://docs.microsoft.com/en-us/rest/api/storageservices/service-sas-examples
    params = {
        "st": key["SignedStart"],
        "se": key["SignedExpiry"],
        "sks": key["SignedService"],
        "skt": key["SignedStart"],
        "ske": key["SignedExpiry"],
        "sktid": key["SignedTid"],
        "skoid": key["SignedOid"],
        # signed key version (param name not mentioned in docs)
        "skv": key["SignedVersion"],
        "sv": "2018-11-09",  # signed version
        "sr": "b",  # signed resource
        "sp": "r",  # signed permissions
        "sip": "",  # signed ip
        "si": "",  # signed identifier
        "spr": "https,http",  # signed http protocol
        "rscc": "",  # Cache-Control header
        "rscd": "",  # Content-Disposition header
        "rsce": "",  # Content-Encoding header
        "rscl": "",  # Content-Language header
        "rsct": "",  # Content-Type header
    }
    u = urllib.parse.urlparse(url)
    storage_account = u.netloc.split(".")[0]
    canonicalized_resource = urllib.parse.unquote(
        f"/blob/{storage_account}/{u.path[1:]}"
    )
    parts_to_sign = (
        params["sp"],
        params["st"],
        params["se"],
        canonicalized_resource,
        params["skoid"],
        params["sktid"],
        params["skt"],
        params["ske"],
        params["sks"],
        params["skv"],
        params["sip"],
        params["spr"],
        params["sv"],
        params["sr"],
        params["rscc"],
        params["rscd"],
        params["rsce"],
        params["rscl"],
        params["rsct"],
        # this is documented on a different page
        # https://docs.microsoft.com/en-us/rest/api/storageservices/create-service-sas#specifying-the-signed-identifier
        params["si"],
    )
    string_to_sign = "\n".join(parts_to_sign)
    params["sig"] = base64.b64encode(
        hmac.digest(
            base64.b64decode(key["Value"]), string_to_sign.encode("utf8"), "sha256"
        )
    ).decode("utf8")
    query = urllib.parse.urlencode({k: v for k, v in params.items() if v != ""})
    # convert to a utc struct_time by replacing the timezone
    ts = time.strptime(key["SignedExpiry"].replace("Z", "GMT"), "%Y-%m-%dT%H:%M:%S%Z")
    t = calendar.timegm(ts)
    return url + "?" + query, t


def split_path(path: str) -> Tuple[str, str, str]:
    if path.startswith("az://"):
        return split_az_path(path)
    elif path.startswith("https://"):
        return split_https_path(path)
    else:
        raise Error(f"Invalid path: '{path}'")


def split_az_path(path: str) -> Tuple[str, str, str]:
    parts = path[len("az://") :].split("/")
    if len(parts) < 2:
        raise Error(f"Invalid path: '{path}'")
    account = parts[0]
    container = parts[1]
    obj = "/".join(parts[2:])
    return account, container, obj


def split_https_path(path: str) -> Tuple[str, str, str]:
    parts = path[len("https://") :].split("/")
    if len(parts) < 2:
        raise Error(f"Invalid path: '{path}'")
    hostname = parts[0]
    container = parts[1]
    if not hostname.endswith(".blob.core.windows.net") or container == "":
        raise Error(f"Invalid path: '{path}'")
    obj = "/".join(parts[2:])
    account = hostname.split(".")[0]
    return account, container, obj


def combine_https_path(account: str, container: str, obj: str) -> str:
    return f"https://{account}.blob.core.windows.net/{container}/{obj}"


def combine_az_path(account: str, container: str, obj: str) -> str:
    return f"az://{account}/{container}/{obj}"


def sign_with_shared_key(req: Request, key: str) -> str:
    # https://docs.microsoft.com/en-us/rest/api/storageservices/authorize-with-shared-key
    params_to_sign = []
    if req.params is not None:
        for name, value in req.params.items():
            canonical_name = name.lower()
            params_to_sign.append(f"{canonical_name}:{value}")

    u = urllib.parse.urlparse(req.url)
    storage_account = u.netloc.split(".")[0]
    canonical_url = f"/{storage_account}/{u.path[1:]}"
    canonicalized_resource = "\n".join([canonical_url] + list(sorted(params_to_sign)))

    if req.headers is None:
        headers = {}
    else:
        headers = dict(req.headers)

    headers_to_sign = []
    for name, value in headers.items():
        canonical_name = name.lower()
        canonical_value = re.sub(r"\s+", " ", value).strip()
        if canonical_name.startswith("x-ms-"):
            headers_to_sign.append(f"{canonical_name}:{canonical_value}")
    canonicalized_headers = "\n".join(sorted(headers_to_sign))

    content_length = headers.get("Content-Length", "")
    if req.data is not None:
        content_length = str(len(req.data))

    parts_to_sign = [
        req.method,
        headers.get("Content-Encoding", ""),
        headers.get("Content-Language", ""),
        content_length,
        headers.get("Content-MD5", ""),
        headers.get("Content-Type", ""),
        headers.get("Date", ""),
        headers.get("If-Modified-Since", ""),
        headers.get("If-Match", ""),
        headers.get("If-None-Match", ""),
        headers.get("If-Unmodified-Since", ""),
        headers.get("Range", ""),
        canonicalized_headers,
        canonicalized_resource,
    ]
    string_to_sign = "\n".join(parts_to_sign)

    signature = base64.b64encode(
        hmac.digest(base64.b64decode(key), string_to_sign.encode("utf8"), "sha256")
    ).decode("utf8")

    return f"SharedKey {storage_account}:{signature}"
