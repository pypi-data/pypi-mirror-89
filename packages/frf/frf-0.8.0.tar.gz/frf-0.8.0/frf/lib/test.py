"""Declares :class:`ResourceEndpointTestCase`."""
import copy
import unittest

import ioc
import unimatrix.ext.jose.__ioc__
from unimatrix.ext import jose
from unimatrix.ext.jose.tests import signer
from fastapi.testclient import TestClient

import frf


class ResourceEndpointTestCase(unittest.TestCase):
    """Provides boilerplate to test :class:`~frf.Resource` objects."""
    endpoints = []

    def setUp(self):
        # TODO: Hack
        unimatrix.ext.jose.__ioc__.setup_ioc()
        self.asgi = self.get_asgi_application()
        for path, cls in self.endpoints:
            self.asgi.add_resource(cls, base_path=path)
        self.client = TestClient(self.asgi)

    def request(self, func, *args, **kwargs):
        headers = kwargs.pop('headers', None) or {}
        return func(*args, headers={**headers, **copy.deepcopy(self.headers)},
            **kwargs)

    def get_headers(self):
        """Return the default headers."""
        return {}

    def get_asgi_application(self):
        """Return the :class:`~frf.ASGIApplication` instance that is used
        during this test. Subclasses must override this method.
        """
        raise NotImplementedError


class ProtectedResourceTestCase(ResourceEndpointTestCase):
    audience = None
    scopes = None

    @property
    def headers(self):
        return {
            'Authorization': f"Bearer {bytes.decode(self.token)}"
        }

    def setUp(self):
        super().setUp()
        self.signer = signer.HMACSigner()
        self.jwt = jose.jwt.sync({'aud': self.audience, 'sub': 'foo'},
            signer=self.signer)
        self.token = bytes(self.jwt)

    def refresh_token(self, aud=None, claims=None, scopes=None, **kwargs):
        claims = {'sub': 'foo', **(claims or {})}
        if scopes is not None:
            claims['scopes'] = scopes
        if aud is not None:
            claims['aud'] = aud
        self.jwt = jose.jwt.sync(claims, signer=self.signer)
        self.token = bytes(self.jwt)
