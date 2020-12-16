"""
.. module:: account
   :synopsis: Account module.
"""
from datetime import datetime

import six

from vivialconnect.resources.resource import Resource
from vivialconnect.resources.countable import Countable
from vivialconnect.common.util import Util

_TRANSACTION_SEARCH_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


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


class Transaction(Resource):
    """
        Represents a system transaction.

        Transaction properties

        ================  ==================================================================
        Field             Description
        ================  ==================================================================
        id                Id of the transaction.
        account_id        Id of the account.
        balances          Total cash or credits spent in the account.
        cash_amount       Amount spent equivalent to ten thousand cents.
        credit_amount     Credits spent in the transaction.
        data              Metadata of the transaction. It differs for each transaction type.
        post_time         Date when the transaction was issued.
        transaction_type  Type of the transaction.
        unit_count        Number of times of this transaction.
        ================  ==================================================================
    """


    @classmethod
    def find(cls, id_=None, path=None, **kwargs):
        """
            Retrieve one or a list of transactions from the user account.

            :param id_: Search a transaction using an ID.
            :type id_: ``int``
            :param start_time: *Passed as kwargs*. Start date and time in ISO 8601 format like YYYYMMDDThhmmssZ
            :type start_time: ``str``
            :param end_time:  *Passed as kwargs*. End date and time in ISO 8601 format like YYYYMMDDThhmmssZ
            :type end_time: ``str``
            :param transaction_type: *Passed as kwargs*. Filter transactions by type (see allowed types below).
            :type transaction_type: ``str``
            :param \**kwargs: Include optional keywords like page, limit,etc. and other useful keys for searching.

            :returns: a transaction object or a list of transaction objects.
            :raises: :class:`BadRequest`: If the transaction ID is not found.

            Allowed transaction types:
                - mms_local_in
                - mms_local_out
                - mms_shortcode_in
                - mms_shortcode_out
                - mms_tollfree_in
                - mms_tollfree_out
                - number_purchase
                - number_purchase_tollfree
                - number_release
                - number_renew
                - number_renew_tollfree
                - sms_intl_out
                - sms_local_in
                - sms_local_out
                - sms_shortcode_in
                - sms_shortcode_out
                - sms_tollfree_in
                - sms_tollfree_out
                - voice_forward
                - voice_forward_tollfree

        """
        if id_:
            return cls._find_single(id_)
        if "transaction_type" in kwargs:
            transaction_types = kwargs.pop("transaction_type")
            kwargs["include_types[]"] = transaction_types
        if "start_time" not in kwargs and "end_time" not in "end_time":
            year_ago = datetime.now().year - 1
            start_time = datetime.now().replace(year=year_ago).strftime(_TRANSACTION_SEARCH_DATE_FORMAT)
            end_time = datetime.now().strftime(_TRANSACTION_SEARCH_DATE_FORMAT)
            kwargs["start_time"] = start_time
            kwargs["end_time"] = end_time
        transactions = cls._find_every(root="transactions", **kwargs)
        return transactions

