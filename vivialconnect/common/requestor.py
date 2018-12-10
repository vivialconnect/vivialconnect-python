"""
.. module:: requestor
   :synopsis: Requestor module.

"""

import json
import hmac
import time
import types
import hashlib
import platform
import datetime

import six
from six.moves.urllib.parse import urlencode, quote_plus, urlparse, parse_qsl, quote

try:
    import requests
except ImportError:
    raise ImportError(
        "requests library is required. "
        + 'Install requests via "pip install requests".'
    )

from vivialconnect.version import VERSION
from vivialconnect.common.error import (
    RequestorError,
    Redirection,
    RateLimit,
    BadRequest,
    UnauthorizedAccess,
    ForbiddenAccess,
    ResourceNotFound,
    MethodNotAllowed,
    ResourceConflict,
    ResourceInvalid,
    ClientError,
    ServerError,
)
from vivialconnect.common.util import Util


API_BASE_URL = "https://api.vivialconnect.net/api/v1.0"
API_KEY = ""
API_SECRET = ""
API_ACCOUNT_ID = ""

API_HMAC_SIGNED_HEADERS = ["content-type", "date", "host"]
API_CONTENT_TYPE = "application/json"


class Requestor(object):
    def __init__(
        self,
        api_key=None,
        api_secret=None,
        api_base_url=None,
        api_account_id=None,
        request_timeout=None,
        verify_request=True,
    ):
        self.api_key = api_key if api_key else API_KEY
        self.api_secret = api_secret if api_secret else API_SECRET
        self.api_base_url = api_base_url if api_base_url else API_BASE_URL
        self.api_account_id = api_account_id if api_account_id else API_ACCOUNT_ID
        self.request_timeout = request_timeout if request_timeout else 30
        self.verify_request = verify_request if verify_request is not None else True

    def api_url(self, url=None):
        url = url or ""
        return "%s%s" % (self.api_base_url, url)

    @classmethod
    def _str_to_bytes(cls, s):
        if six.PY2:
            if isinstance(s, unicode):
                return s.encode()
        else:
            if isinstance(s, str):
                return s.encode()
        return s

    @classmethod
    def _bytes_to_str(s):
        if six.PY3:
            if isinstance(s, bytes):
                return s.decode()
        return s

    @classmethod
    def _utf8(cls, value):
        if six.PY2:
            # Python2's urlencode wants bytestrings, not unicode
            if isinstance(value, six.text_type):
                return value.encode("utf-8")
            return value
        elif isinstance(value, six.binary_type):
            # Python3's six.text_type(bytestring) returns "b'bytestring'"
            # So, have to decode it to unicode
            return value.decode("utf-8")
        else:
            # Python3's urlencode can handle unicode
            return value

    @classmethod
    def _uri_encode(cls, data, encode_slash=False):
        safe = "_-~."
        if not encode_slash:
            safe += "/"
        return quote(data, safe=safe)

    @classmethod
    def encode_dict(cls, out, key, dict_value):
        n = {}
        for k, v in six.iteritems(dict_value):
            k = cls._utf8(k)
            v = cls._utf8(v)
            n["%s[%s]" % (key, k)] = v
        out.extend(cls._encode_inner(n))

    @classmethod
    def encode_list(cls, out, key, list_value):
        n = {}
        for k, v in enumerate(list_value):
            v = cls._utf8(v)
            n["%s[%s]" % (key, k)] = v
        out.extend(cls._encode_inner(n))

    @classmethod
    def encode_datetime(cls, out, key, dt_value):
        utc_timestamp = int(time.mktime(dt_value.timetuple()))
        out.append((key, utc_timestamp))

    @classmethod
    def encode_none(cls, out, key, value):
        pass  # do not include None-valued params in request

    @classmethod
    def _encode_inner(cls, params):
        # special case value encoding
        ENCODERS = {
            list: cls.encode_list,
            dict: cls.encode_dict,
            datetime.datetime: cls.encode_datetime,
        }
        if six.PY2:
            ENCODERS[types.NoneType] = cls.encode_none
        if six.PY3:
            ENCODERS[type(None)] = cls.encode_none

        out = []
        for key, value in six.iteritems(params):
            key = cls._utf8(key)
            try:
                encoder = ENCODERS[value.__class__]
                encoder(out, key, value)
            except KeyError:
                # don't need special encoding
                try:
                    value = six.text_type(value)
                except:
                    pass

                out.append((key, value))
        return out

    @classmethod
    def encode(cls, params):
        return urlencode(cls._encode_inner(params))

    @classmethod
    def encode_body(cls, params=None):
        return cls._utf8(Util.to_json(params, root=None))

    @classmethod
    def build_url(cls, url, params):
        base_query = urlparse(url).query
        if base_query:
            return "%s&%s" % (url, cls.encode(params))
        else:
            return "%s?%s" % (url, cls.encode(params))

    def sign(self, method, iso8601_timestamp, abs_url, headers, data):
        if self.api_secret is None:
            raise RequestorError("No API secret provided.")

        api_hmac_used_signed_headers = []
        canonical_headers = []
        for key in headers.keys():
            if key.lower() in API_HMAC_SIGNED_HEADERS:
                canonical_headers.append(key.lower() + ":" + headers[key])
                api_hmac_used_signed_headers.append(key.lower())
        api_hmac_used_signed_headers.sort()
        canonical_headers.sort()

        parsed_url = urlparse(abs_url)

        # Parse query string
        canonical_query_string = []
        query_string = parse_qsl(
            parsed_url.query, keep_blank_values=True, strict_parsing=False
        )
        for item in query_string:
            canonical_query_string.append(
                self._uri_encode(item[0], encode_slash=True)
                + "="
                + self._uri_encode(item[1], encode_slash=True)
            )
        canonical_query_string.sort()

        canonical_request = (
            method.upper()
            + "\n"
            + iso8601_timestamp
            + "\n"
            + self._uri_encode(parsed_url.path, encode_slash=False)
            + "\n"
            + "&".join(canonical_query_string)
            + "\n"
            + "\n".join(canonical_headers)
            + "\n"
            + ";".join(api_hmac_used_signed_headers).lower()
            + "\n"
            + hashlib.sha256(self._str_to_bytes(data if data else "")).hexdigest()
        )

        h = hmac.new(self._str_to_bytes(self.api_secret), b"", hashlib.sha256)
        h.update(self._str_to_bytes(canonical_request))

        return h.hexdigest(), api_hmac_used_signed_headers

    def request(self, method, url, params=None, **kwargs):
        if params is None:
            params = {}
        http_body, http_status, response_url, response_headers = self.request_raw(
            method, url, params, **kwargs
        )
        response = self.interpret_response(
            http_body, http_status, response_url, response_headers
        )
        return response

    def get(self, url, params=None, **kwargs):
        return self.request("get", url, params, **kwargs)

    def put(self, url, params=None, **kwargs):
        return self.request("put", url, params, **kwargs)

    def post(self, url, params=None, **kwargs):
        return self.request("post", url, params, **kwargs)

    def delete(self, url, params=None, **kwargs):
        return self.request("delete", url, params, **kwargs)

    def head(self, url, params=None, **kwargs):
        return self.request("head", url, params, **kwargs)

    def request_raw(self, method, url, params=None, **kwargs):
        if params is None:
            params = {}
        now = datetime.datetime.utcnow()
        abs_url = self.api_url(url)

        method = method.lower()
        if method == "get" or method == "delete":
            if params:
                abs_url = self.build_url(abs_url, params)
            data = None
        elif method == "post" or method == "put":
            data = self.encode_body(params)
        else:
            raise RequestorError(
                "Bug discovered: invalid request method: %s. "
                "Please report to contact@vivialconnect.net." % method
            )

        ua = {
            "client_version": VERSION,
            "lang": "python",
            "publisher": "vivialconnect",
            "request_lib": "requests",
        }

        for attr, func in [
            ["lang_version", platform.python_version],
            ["platform", platform.platform],
        ]:
            try:
                val = func()
            except Exception as e:
                val = "!! %s" % e
            ua[attr] = val

        parsed_url = urlparse(abs_url)
        headers = {
            "X-VivialConnect-User-Agent": json.dumps(ua),
            "User-Agent": "VivialConnect PythonClient %s" % VERSION,
            "Date": "%s" % (now.strftime("%a, %d %b %Y %H:%M:%S GMT")),
            "Host": parsed_url.hostname
            + ((":" + str(parsed_url.port)) if parsed_url.port else ""),
            "Accept": API_CONTENT_TYPE,
        }

        if data:
            headers["Content-Type"] = API_CONTENT_TYPE
        elif method in ["post", "put"]:
            headers["Content-Type"] = API_CONTENT_TYPE
            headers["Content-Length"] = "0"

        iso8601_timestamp = now.strftime("%Y%m%dT%H%M%SZ")
        digest, api_hmac_used_signed_headers = self.sign(
            method, iso8601_timestamp, abs_url, headers, data
        )
        headers["X-Auth-SignedHeaders"] = "%s" % (
            ";".join(api_hmac_used_signed_headers).lower()
        )
        headers["X-Auth-Date"] = iso8601_timestamp
        headers["Authorization"] = "HMAC %s%s" % (
            str(self.api_key) + ":" if self.api_key else "",
            digest,
        )

        http_body, http_status, response_url, response_headers = self.requests_request(
            method, abs_url, headers, data, **kwargs
        )

        return http_body, http_status, response_url, response_headers

    def interpret_response(
        self, http_body, http_status, response_url, response_headers
    ):
        # 204 should return empty body only, so let's check
        # if we are getting anything else back.
        if http_status == 204 and not http_body:
            return http_body
        try:
            loaded_response = json.loads(http_body)
        except Exception:
            raise RequestorError(
                "Invalid JSON response body from API: (%d) %s "
                % (http_status, http_body),
                http_status,
                http_body,
            )
        if not (200 <= http_status < 300):
            self._handle_api_error(
                http_status, http_body, loaded_response, response_url, response_headers
            )
        return loaded_response

    def requests_request(self, method, abs_url, headers, data, **kwargs):
        try:
            result = requests.request(
                method,
                abs_url,
                headers=headers,
                data=data,
                timeout=self.request_timeout,
                verify=self.verify_request,
                **kwargs
            )
            http_body = result.text
            http_status = result.status_code
            response_url = result.url
            response_headers = result.headers
        except Exception as e:
            raise RequestorError(
                "Unexpected error communicating with VivialConnect. If this "
                "problem persists please let us know at contact@vivialconnect.net."
            )
        return http_body, http_status, response_url, response_headers

    def _handle_api_error(
        self, http_status, http_body, loaded_response, response_url, response_headers
    ):
        if loaded_response and isinstance(loaded_response, dict):
            try:
                if "error" in loaded_response:
                    message = loaded_response["error"]
                    if isinstance(message, dict) and "message" in message:
                        message = message.get(
                            "message",
                            "Invalid response from API: (%d) %s"
                            % (http_status, loaded_response_url),
                        )
                else:
                    message = loaded_response["message"]
            except (KeyError, TypeError):
                message = "Invalid response from API: (%d) %s" % (
                    http_status,
                    response_url,
                )
        else:
            message = str(loaded_response)

        if http_status in (301, 302):
            raise Redirection(
                message, http_status, http_body, response_url, response_headers
            )
        elif http_status == 400:
            raise BadRequest(message, http_status, http_body)
        elif http_status == 401:
            raise UnauthorizedAccess(message, http_status, http_body)
        elif http_status == 403:
            raise ForbiddenAccess(message, http_status, http_body)
        elif http_status == 404:
            raise ResourceNotFound(message, http_status, http_body)
        elif http_status == 405:
            raise MethodNotAllowed(message, http_status, http_body)
        elif http_status == 409:
            raise ResourceConflict(message, http_status, http_body)
        elif http_status == 422:
            raise ResourceInvalid(message, http_status, http_body)
        elif http_status == 429:
            raise RateLimit(message, http_status, http_body)
        elif 401 <= http_status < 500:
            raise ClientError(message, http_status, http_body)
        elif 500 <= http_status < 600:
            raise ServerError(message, http_status, http_body)
        else:
            raise RequstorError(message, http_status, http_body)
