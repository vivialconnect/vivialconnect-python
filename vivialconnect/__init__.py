"""Vivial Connect is an application programming interface (API) that enables
    text messaging capabilities for client applications.

.. moduleauthor:: Boris Musa <boris@vivialconnect.net>

"""

try:
    from version import VERSION

    __vivialconnet_version__ = VERSION
except ImportError:
    __vivialconnet_version__ = "vivialconnect-dev"

from vivialconnect.resources.resource import Resource
from vivialconnect.common.requestor import Requestor

from vivialconnect.resources.user import User
from vivialconnect.resources.account import Account
from vivialconnect.resources.message import Message, Attachment
from vivialconnect.resources.number import Number
from vivialconnect.resources.connector import (
    Connector,
    ConnectorNumber,
    ConnectorCallback,
)

from vivialconnect.resources.log import Log
