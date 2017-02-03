"""
.. module:: user
   :synopsis: User module.
"""

from vivialconnect.resources.resource import Resource
from vivialconnect.resources.countable import Countable


class User(Resource, Countable):
    """Use the User resource to manage users and user passwords in the API.
    """
    pass
