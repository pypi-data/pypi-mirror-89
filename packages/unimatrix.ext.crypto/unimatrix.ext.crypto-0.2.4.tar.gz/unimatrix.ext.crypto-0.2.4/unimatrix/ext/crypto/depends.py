"""Declares dependencies for use with :mod:`fastapi`."""
try:
    from fastapi import Depends

    __all__ [
        'SessionCookie'
    ]
except ImportError:
    __all__ = []


def SessionCookie(cookie_name='sessionid', required=True):
    def f(sessionid: str = Cookie(None, alias=cookie_name)):
        signature = JSONWebSignature.parse(str.encode(sessionid))
        if not signature.verify(SecretKey.default()):
            signature = None
            if required:
                raise ActiveSessionRequired
        return signature
    return Depends(f)
