"""
.. module:: number
   :synopsis: Number module.
"""

from vivialconnect.resources.resource import Resource
from vivialconnect.resources.countable import Countable
from vivialconnect.common.util import Util


class Number(Resource, Countable):
    """The :class:`Number` resource provides functionality to work with account
        associated and available phone numbers.

        Purchasing a Phone Number

        Before you can send or receive text messages using Vivial Connect, you must
        purchase at least one phone number and associate it with your account. The
        API lets you choose from a list of US-only, non-toll-free available numbers.
        When you query this list to find an available number that meets your needs,
        you can tailor your search to target specific criteria, including:

        * the city, US state, area code, or ZIP code where the number is located
        * a number pattern you specify containing wildcards for individual digits
        * an alphanumeric pattern you specify (for choosing numbers that spell a word)
    """

    @classmethod
    def available(cls, opts=None, **kwargs):
        """Lists available phone numbers.

        :param opts: Additional query params.
        :type opts: ``dict``.
        :param \**kwargs: You must specify exactly one of the following three keys:
            in_region, area_code, in_postal_code.

        :returns: :class:`Number` -- a list of available US local (non-toll-free) phone numbers.
        """
        qs = {}
        country_code = 'US'
        number_type = 'local'
        if opts is None:
            opts = kwargs
        for k in opts.keys():
            if k == 'country_code' and opts[k]:
                country_code = opts[k].upper()
            elif k == 'number_type' and opts[k]:
                number_type = opts[k].lower()
            else:
                if opts[k]:
                    qs[k] = opts[k]
        url = cls._custom_path(
            custom_path="/available/{}/{}".format(country_code, number_type))
        return cls._build_list(Number.request.get(url, qs))

    def buy(self):
        """Purchases a new phone number.
        """
        return self.save()

    def buy_local(self):
        """Purchases a new local phone number.
        """
        self.phone_number_type = 'local'
        return self.save()

Number._singular = 'phone_number'
