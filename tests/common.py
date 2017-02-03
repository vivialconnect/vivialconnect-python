import os
import re
import sys
import json
import unittest
import datetime
from functools import wraps

import requests
from requests import cookies
from requests import structures

from six import string_types, binary_type
from six.moves.urllib.parse import urlsplit

from vivialconnect.version import VERSION
from vivialconnect.resources.resource import Resource


class Headers(object):
    def __init__(self, res):
        self.headers = res.headers

    def get_all(self, name, failobj=None):
        return self.getheaders(name)

    def getheaders(self, name):
        return [self.headers.get(name)]


def response(status_code=200, content='', headers=None, reason=None, elapsed=0,
             request=None):
    res = requests.Response()
    res.status_code = status_code
    if isinstance(content, (dict, list)):
        if sys.version_info[0] == 3:
            content = bytes(json.dumps(content), 'utf-8')
        else:
            content = json.dumps(content)
    res._content = content
    res._content_consumed = content
    res.headers = structures.CaseInsensitiveDict(headers or {})
    res.reason = reason
    res.elapsed = datetime.timedelta(elapsed)
    res.request = request
    if hasattr(request, 'url'):
        res.url = request.url
        if isinstance(request.url, bytes):
            res.url = request.url.decode('utf-8')
    if 'set-cookie' in res.headers:
        res.cookies.extract_cookies(cookies.MockResponse(Headers(res)),
                                    cookies.MockRequest(request))

    # normally this closes the underlying connection,
    # but we have nothing to free.
    res.close = lambda *args, **kwargs: None

    return res


def all_requests(func):
    @wraps(func)
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner


def first_of(handlers, *args, **kwargs):
    for handler in handlers:
        try:
            res = handler(*args, **kwargs)
        except Exception as e:
            raise e
        if res is not None:
            return res


class HTTMock(object):
    """
    Acts as a context manager to allow mocking
    """
    STATUS_CODE = 200

    def __init__(self, *handlers, **kwargs):
        self.handlers = handlers
        self.kwargs = kwargs

    def __enter__(self):
        self._real_session_send = requests.Session.send
        self._real_session_prepare_request = requests.Session.prepare_request

        def _fake_send(session, request, **kwargs):
            response = self.intercept(request)
            if isinstance(response, requests.Response):
                # this is pasted from requests to handle redirects properly:
                kwargs.setdefault('stream', session.stream)
                kwargs.setdefault('verify', session.verify)
                kwargs.setdefault('cert', session.cert)
                kwargs.setdefault('proxies', session.proxies)

                allow_redirects = kwargs.pop('allow_redirects', True)
                stream = kwargs.get('stream')
                timeout = kwargs.get('timeout')
                verify = kwargs.get('verify')
                cert = kwargs.get('cert')
                proxies = kwargs.get('proxies')

                gen = session.resolve_redirects(
                    response,
                    request,
                    stream=stream,
                    timeout=timeout,
                    verify=verify,
                    cert=cert,
                    proxies=proxies)

                history = [resp for resp in gen] if allow_redirects else []

                if history:
                    history.insert(0, response)
                    response = history.pop()
                    response.history = tuple(history)
                return response

            return self._real_session_send(session, request, **kwargs)

        def _fake_prepare_request(session, request):
            """
            Fake this method so the `PreparedRequest` objects contains
            an attribute `original` of the original request.
            """
            prep = self._real_session_prepare_request(session, request)
            prep.original = request
            return prep

        requests.Session.send = _fake_send
        requests.Session.prepare_request = _fake_prepare_request

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        requests.Session.send = self._real_session_send
        requests.Session.prepare_request = self._real_session_prepare_request

    def intercept(self, request):
        url = urlsplit(request.url)
        res = first_of(self.handlers, url, request, **self.kwargs)
        if isinstance(res, requests.Response):
            return res
        elif isinstance(res, dict):
            return response(res.get('status_code'),
                            res.get('content'),
                            res.get('headers'),
                            res.get('reason'),
                            res.get('elapsed', 0),
                            request)
        elif isinstance(res, string_types) or isinstance(res, binary_type):
            return response(content=res)
        elif res is None:
            return None
        else:
            raise TypeError(
                "Dont know how to handle response of type {0}".format(type(res)))

def with_httmock(*handlers):
    mock = HTTMock(*handlers)

    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            with mock:
                return func(*args, **kwargs)
        return inner
    return decorator

class BaseTestCase(unittest.TestCase):

    def setUp(self):
        Resource.api_account_id = "1234567890"
        Resource.api_key = "__my_test_key__"
        Resource.api_secret = "__my_test_secret__"
        Resource.api_base_url = "https://tests.vivialconnect.net/api/v1.0"

    @all_requests
    def response_content(self, url, request, **kwargs):
        return self.fake(url, request, **kwargs)

    def load_fixture(self, name, frmt='json'):
        with open(os.path.dirname(__file__) + '/fixtures/%s.%s' % (name, frmt), 'rb') as f:
            return f.read()

    def fake(self, url, request, **kwargs):
        endpoint = kwargs.pop('endpoint', None)
        frmt = kwargs.pop('frmt', 'json')
        body = kwargs.pop('body', None) or (self.load_fixture(
            endpoint, frmt=frmt) if endpoint else '')

        headers = {}
        if kwargs.pop('has_user_agent', True):
            headers['User-Agent'] = 'VivialConnectPythonAPI/%s Python/%s' % (
                VERSION, sys.version.split(' ', 1)[0])

        try:
            headers.update(kwargs['headers'])
        except KeyError:
           pass

        code = kwargs.pop('code', 200)
        reason = kwargs.pop('reason', None)
        elapsed = kwargs.pop('elapsed', 0)

        return response(
            status_code=code, content=body, headers=headers,
            reason=reason, elapsed=elapsed, request=request
            )
