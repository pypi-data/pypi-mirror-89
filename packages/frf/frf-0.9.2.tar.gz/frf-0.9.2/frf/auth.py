"""Supplies authentication functions."""
from fastapi import Cookie
from fastapi import Depends
from fastapi import Request

from unimatrix.ext import crypto
from unimatrix.ext import jose

from .exceptions import BearerTokenMissing
from .exceptions import InvalidAuthorizationScheme
from .exceptions import BearerTokenUnverifiable


def get_bearer_token(request: Request):
    header = request.headers.get('Authorization')
    value = None
    if header:
        scheme, _, value = str.partition(header, ' ')
        if str.lower(scheme) != 'bearer':
            raise InvalidAuthorizationScheme(scheme, ['Bearer'])
    return value


def RequestClaims(allow_cookies=False, cookie_name='sessionid', required=True):
    async def f(request: Request, bearer=Bearer, sessionid:str=Cookie(None)):
        if not bearer and allow_cookies:
            bearer = request.cookies.get(cookie_name)
        if not bearer and required:
            raise BearerTokenMissing

        if bearer:
            try:
                return await jose.payload(str.encode(bearer))
            except crypto.Signature.InvalidSignature:
                if required:
                    raise BearerTokenUnverifiable

    return Depends(f)


Bearer = Depends(get_bearer_token)
