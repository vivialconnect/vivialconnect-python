"""
.. module:: error
   :synopsis: The following error classes exist in the
              Vivial Connect API.
"""

import json


class RequestorError(Exception):
    """Base Requestor Error
    """

    def __init__(self, message=None, http_status=None, http_body=None):
        self.http_status = http_status
        self.http_body = http_body
        try:
            self.json_body = json.loads(http_body)
        except:
            self.json_body = None

        if "error_code" in self.json_body:
            super(RequestorError, self).__init__(
                "{}: {}".format(self.json_body.get("error_code"), message)
            )
        else:
            super(RequestorError, self).__init__(message)

        self.param = None
        try:
            self.param = self.json_body["error"].get("param", None)
        except:
            pass


# HTTP error code 5xx (500..599)
class ServerError(RequestorError):
    """Any 5xx HTTP Error 5xx (500..599)

    Raised if an internal server error occurred.
    """

    pass


# Network connection error
class ConnectionError(RequestorError):
    """Network Connection Error

    This error is raised if Vivial Connect API client detects
    a connection error.
    """

    pass


# HTTP 3xx redirection
class Redirection(ConnectionError):
    """3xx Redirection Error

    Raised for all HTTP redirects.
    """

    def __init__(
        self, message=None, http_status=None, http_body=None, url=None, headers=None
    ):
        super(Redirection, self).__init__(message, http_status, http_body)
        self.url = url
        self.headers = headers


# HTTP error 4xx (401..499)
class ClientError(ConnectionError):
    """4xx Base HTTP Error (401..499)

    Baseclass for all 4xx exceptions.
    """

    pass


# 409 Conflict
class ResourceConflict(ClientError):
    """409 Resource Conflict

    Raised if there is resource conflict.
    """

    pass


# 422 Resource Invalid
class ResourceInvalid(ClientError):
    """422 Resource Invalid

    Raised if a resource is invalid.
    """

    pass


# 429 Rate Limit
class RateLimit(ClientError):
    """429 Rate Limit

    Raised if rate limit reached.
    """

    pass


# 404 Resource Not Found
class ResourceNotFound(ClientError):
    """404 Resource Not Found

    Raised if a resource does not exist.
    """

    pass


# 400 Bad Request
class BadRequest(ClientError):
    """400 Bad Request

    Raised if the client receives something and cannot handle it.
    """

    pass


# 401 Unauthorized
class UnauthorizedAccess(ClientError):
    """401 Unauthorized

    Raised if the user is not authorized to access remote resource.
    """

    pass


# 403 Forbidden
class ForbiddenAccess(ClientError):
    """403 Forbidden

    Raised if the user doesn't have the permission for the
    requested resource.
    """

    pass


# 405 Method Not Allowed
class MethodNotAllowed(ClientError):
    """405 Method Not Allowed

    Raised if the server does not handle method used to access resource.
    For example POST if the resource is view only.
    """

    pass


class ResourceError(Exception):
    """Generic Resource Error

    Raised if there is an error while processing response JSON data.
    """

    def __init__(self, message=None):
        super(ResourceError, self).__init__(message)
