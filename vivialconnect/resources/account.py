"""
.. module:: account
   :synopsis: Account module.
"""

import six

from vivialconnect.resources.resource import Resource
from vivialconnect.resources.countable import Countable
from vivialconnect.common.util import Util


class Account(Resource, Countable):
    """The Account resource is used for managing accounts and sub-accounts in the API.

    Example request to retrieve a billing status for account id 12345::

        from vivialconnect import Resource, Account

        Resource.api_key = ""
        Resource.api_secret = ""
        Resource.api_account_id = "12345"

        def billing_status(account_id=None):
            status = Account.billing_status(account_id=account_id)
            print(status)

        billing_status(12345)

    Example request to retrieve a list of sub-accounts for the main account::

        from vivialconnect import Resource, Account

        Resource.api_key = ""
        Resource.api_secret = ""
        Resource.api_account_id = "12345"

        def list_subaccounts():
            subaccounts = Account.subaccounts()
            for subaccount in subaccounts:
                print(subaccount.id)

        list_subaccounts()
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
        return cls.request.get('/accounts/%s/status.json' % (account_id))

    @classmethod
    def subaccounts(cls, opts=None, **kwargs):
        """Returns the list of all sub-accounts in the account specified in
        the ``Resource.api_account_id`` parameter.

        :param opts: Additional query params.
        :type opts: ``dict``.
        :param \**kwargs: Additional arguments.

        :returns: ``list`` -- retrieves a list of sub-accounts for the main account.
        """
        resources = []
        if opts is None:
            opts = kwargs
        attributes = cls.request.get(
            '/accounts/%s/subaccounts.json' % Resource.api_account_id, opts)
        account = Util.remove_root(attributes)
        elements = account['accounts'] if 'accounts' in account else []
        if isinstance(elements, dict):
            elements = [elements]
        for element in elements:
            resources.append(cls(Util.remove_root(element)))
        return resources
