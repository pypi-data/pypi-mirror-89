"""Declares common exceptions for the :mod:`unimatrix.ext.crypto.lib.jose`
package.
"""
from unimatrix.ext.model.exc import CanonicalException


class BaseJoseException(CanonicalException):
    message = "The presented JSON Web Token (JWT) is not valid."


class Expired(BaseJoseException):
    code = 'CREDENTIAL_EXPIRED'
    http_status_code = 403
    message = "The JSON Web Token (JWT) is expired."
    hint = "Provide a valid token."

    def __init__(self, token, now):
        detail = (
            f"At {now}, the token was expired for {int(now-token.exp)} "
            f"seconds."
        )
        super().__init__(detail=detail)


class InvalidAudience(BaseJoseException):
    code = 'INVALID_AUDIENCE'
    http_status_code = 403

    def __init__(self, token, audiences):
        self.token = token
        if not token.aud:
            detail = "The `aud` claim is not specified."
        else:
            detail = (
                f"The audiences specified by the `aud` claim are not valid: "
                f"{str.join(',', token.aud)}"
            )
        hint = (
            f"Present a token with any of the following audiences: "
            f"{str.join(',', audiences)}"
        )
        super().__init__(detail=detail, hint=hint)


class MalformedToken(BaseJoseException):
    code = 'MALFORMED_TOKEN'
    http_status_code = 403
    detail = "The token is malformed and could not be interpreted."
