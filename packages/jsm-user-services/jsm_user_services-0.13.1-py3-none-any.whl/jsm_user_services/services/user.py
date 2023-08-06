import hashlib
from importlib import import_module
from typing import List
from typing import Optional

from jsm_user_services.support.auth_jwt import get_decoded_jwt_token
from jsm_user_services.support.http_utils import get_response_body
from jsm_user_services.support.http_utils import request
from jsm_user_services.support.local_threading_utils import get_from_local_threading
from jsm_user_services.support.request_id import current_request_id


def jwt_has_required_roles(jwt_required_roles: List[str], assert_all=True) -> bool:
    """
    Asserts that the jwt token has all the required roles.
    """
    jsm_token_data = get_jsm_user_data_from_jwt()

    if not jsm_token_data:
        return False

    try:
        jwt_token_roles = jsm_token_data["roles"]
    except KeyError:
        return False

    if not jwt_token_roles:
        return False

    if assert_all:
        return all([(jwt_token_role in jwt_required_roles) for jwt_token_role in jwt_token_roles])

    return any([(jwt_token_role in jwt_required_roles) for jwt_token_role in jwt_token_roles])


def current_jwt_token() -> Optional[str]:
    return get_from_local_threading("authorization_token")


def get_jsm_token() -> Optional[str]:
    token = current_jwt_token()
    if token:
        return get_decoded_jwt_token(token)["jsm_identity"]

    return None


def get_ltm_token() -> Optional[str]:
    token = current_jwt_token()
    if token:
        return get_decoded_jwt_token(token)["yuntiandu"]

    return None


def get_jsm_user_data_from_jwt() -> Optional[dict]:
    token = get_jsm_token()

    if token:
        return get_decoded_jwt_token(token)

    return None


def get_user_email_from_jwt() -> Optional[str]:
    user_data = get_jsm_user_data_from_jwt()
    if user_data:
        return user_data.get("email")

    return None


def get_user_id_from_jwt() -> Optional[str]:
    user_data = get_jsm_user_data_from_jwt()
    if user_data:
        return user_data.get("uid")

    return None


def get_user_access_as_id_from_jwt() -> Optional[str]:
    user_data = get_jsm_user_data_from_jwt()
    if user_data:
        return user_data.get("fid", None)

    return None


def get_user_data_from_server() -> dict:

    current_token = current_jwt_token()
    headers = {"REQUEST-ID": current_request_id()}
    settings = import_module("jsm_user_services.settings")
    user_url = settings.USER_API_HOST

    if current_token:
        headers["Authorization"] = f"Bearer {current_jwt_token()}"

    with request() as r:
        response = r.get(f"{user_url}/users/me/", headers=headers)
        return get_response_body(response)


def get_user_data_from_cpf(cpf: str) -> dict:

    current_token = current_jwt_token()
    headers = {"REQUEST-ID": current_request_id()}
    settings = import_module("jsm_user_services.settings")
    user_url = settings.USER_API_HOST

    if current_token:
        headers["Authorization"] = f"Bearer {current_jwt_token()}"

    with request() as r:
        response = r.get(f"{user_url}/users/search?cpf={cpf}", headers=headers)
        return get_response_body(response)


def get_user_data_from_id(user_id: str) -> dict:

    current_token = current_jwt_token()
    headers = {"REQUEST-ID": current_request_id()}
    settings = import_module("jsm_user_services.settings")
    user_url = settings.USER_API_HOST

    if current_token:
        headers["Authorization"] = f"Bearer {current_jwt_token()}"

    with request() as r:
        response = r.get(f"{user_url}/users/{user_id}/", headers=headers)

        return get_response_body(response)


def get_cpf_from_jwt() -> Optional[str]:

    email = get_user_email_from_jwt()

    return email.split("@")[0] if email else None


def is_retail_user(user_id: str) -> bool:
    settings = import_module("jsm_user_services.settings")
    user_api_token = settings.USER_API_TOKEN
    user_url = settings.USER_API_HOST

    headers = {"REQUEST-ID": current_request_id(), "Authorization": f"Token {user_api_token}"}

    with request() as r:
        response = r.get(f"{user_url}/users/search/?user_id_ref={user_id}&is_retail_user=True", headers=headers)
        response_content = get_response_body(response)
    return response_content["count"] == 1


def get_user_ip() -> Optional[str]:
    return get_from_local_threading("user_ip")


def get_session_id_from_bearer_token(bearer_token: str) -> str:
    return hashlib.sha1(bearer_token.encode("utf-8")).hexdigest()


def get_user_session_id() -> Optional[str]:
    return get_from_local_threading("user_session_id")
