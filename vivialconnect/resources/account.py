"""
.. module:: account
   :synopsis: Account module.
"""

import six

from vivialconnect.resources.resource import Resource
from vivialconnect.resources.countable import Countable
from vivialconnect.common.util import Util


class Account(Resource, Countable):
    """The Account resource is used for managing accounts in the API.

    Account properties

    =============  ===========
    Field          Description
    =============  ===========
    id             Unique identifier of the account object.
    date_created   Creation date (UTC) of the account in ISO 8601 format.
    date_modified  Last modification date (UTC) of the account in ISO 8601 format.
    account_id     Unique identifier of the parent account. (Null if the account is primary.)
    company_name   Primary account name as it is displayed to users (for example, the name of your company).
    =============  ===========

    Example request to retrieve a billing status for account id 12345::

        from vivialconnect import Resource, Account

        Resource.api_key = ""
        Resource.api_secret = ""
        Resource.api_account_id = "12345"

        def billing_status(account_id=None):
            status = Account.billing_status(account_id=account_id)
            print(status)

        billing_status(12345)
    """

    API_ACCOUNT_PREFIX = ""

    @classmethod
    def billing_status(cls, account_id=None):
        """Get current account status for free trial.

        :param account_id: An account id.
        :type account_id: ``int``.

        :returns: A free trial status.
        """
        if account_id:
            if not isinstance(account_id, six.string_types):
                account_id = str(account_id)
        else:
            account_id = Resource.api_account_id
        return cls.request.get("/accounts/%s/status.json" % (account_id))
