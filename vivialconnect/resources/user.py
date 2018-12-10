"""
.. module:: user
   :synopsis: User module.
"""

from vivialconnect.resources.resource import Resource
from vivialconnect.resources.countable import Countable


class User(Resource, Countable):
    """Use the User resource to manage users and user passwords in the API.

    User properties

    ============= ======================
    Field         Description
    ============= ======================
    id            Unique identifier of the user object.
    date_created  Creation date (UTC) of the user in ISO 8601 format.
    date_modified Last modification date (UTC) of the user in ISO 8601 format.
    account_id    Unique identifier of the account that this user is part of.
    username      User's username for logging in to the account. *Max. length:* 128 characters.
    first_name    User's first name. *Max. length:* 128 characters.
    last_name     User's last name. *Max. length:* 128 characters.
    email         User's email address. *Max. length:* 128 characters.
    ============= ======================

    Example request to retrieve a list of users accociated with the account id 12345::

        from vivialconnect import Resource, User

        Resource.api_key = ""
        Resource.api_secret = ""
        Resource.api_account_id = "12345"

        def list_users():
            users = User.find()
            for user in users:
                print(user.id, user.first_name, user.last_name)

        list_users()

    """

    pass
