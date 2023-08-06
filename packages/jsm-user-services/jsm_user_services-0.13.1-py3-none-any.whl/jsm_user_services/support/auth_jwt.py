import re
from typing import Optional

import jwt


def get_decoded_jwt_token(jwt_token: str) -> dict:
    """
    Gets a decoded JWT token.
    """

    return jwt.decode(jwt_token, verify=False)


def get_bearer_authorization_token(authorization_value: str) -> Optional[str]:
    """
    Retrieve a bearer authorization token from an Authorization header value.

    It expects the header value to be something on the lines of: "Bearer token".

    Examples:
    - get_bearer_authorization_token("Bearer token") # returns "token"
    - get_bearer_authorization_token("bearer token") # returns None
    - get_bearer_authorization_token("Token token") # returns None
    - get_bearer_authorization_token("whatever") # returns None
    """
    match = re.match("Bearer", authorization_value)

    if not match:
        return None

    auth_type_beginning = match.span()[1]
    jwt_token = authorization_value[auth_type_beginning:].strip()

    return jwt_token
