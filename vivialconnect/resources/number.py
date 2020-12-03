"""
.. module:: number
   :synopsis: Number module.
"""

from vivialconnect.resources.resource import Resource
from vivialconnect.resources.countable import Countable
from vivialconnect.common.util import Util


class NumberInfo(Resource):
    """
        Resource used for parsing and handling number lookup response. All the heavy-lifting is on the Resource class.
        Expected properties after parsing:
         - carrier: dictionary with info about the carrier
         - device: dictionary with information about the handheld device if it's available.
         - phone_number: phone number itself.
    """

    pass


class Number(Resource, Countable):
    """The :class:`Number` resource provides functionality to work with account
    associated and available phone numbers.

    Purchasing a Phone Number

    Before you can send or receive text messages using Vivial Connect, you must
    purchase at least one phone number and associate it with your account. The
    API lets you choose from a list of available US local or toll-free numbers.
    When you query this list to find an available number that meets your needs,
    you can tailor your search to target specific criteria, including:

    * the city, US state, area code, or ZIP code where the number is located
    * a number pattern you specify containing wildcards for individual digits
    * an alphanumeric pattern you specify (for choosing numbers that spell a word)

    Available numbers properties

    ================= ===========
    Field             Description
    ================= ===========
    name              Associated phone number as it is displayed to users. *Default format:* Friendly national format: (xxx) yyy-zzzz.
    phone_number      Available phone number in E.164 format (+country code +phone number). For US numbers, the format will be ``+1xxxyyyzzzz``.
    phone_number_type Type of available phone number. *Possible values:* 'local' or 'tollfree'.
    city              City where the available phone number is located.
    region            Two-letter US state abbreviation where the available phone number is located.
    lata              Local address and transport area (LATA) where the available phone number is located.
    rate_center       LATA rate center where the available phone number is located. Usually the same as city.
    ================= ===========

    Associated numbers properties

    =============================  ===========
    Field                          Description
    =============================  ===========
    id                             Unique identifier of the phone number object.
    date_created                   Creation date (UTC) of the phone number in ISO 8601 format.
    date_modified                  Last modification date (UTC) of the phone number in ISO 8601 format.
    account_id                     Unique identifier of the account with the phone number.
    name                           Associated phone number as it is displayed to users. *Default format:* Friendly national format: (xxx) yyy-zzzz.
    phone_number                   Associated phone number in E.164 format (+country code +phone number). For US numbers, the format will be ``+1xxxyyyzzzz``.
    phone_number_type              Type of associated phone number. *Possible values:* 'local' or 'tollfree'.
    status_text_url                URL to receive status requests for messages sent via the API using this associated phone number. *Max. length:* 256 characters.
    sms_configuration_id           Unique identifier of the message status callback configuration to be used to handle SMS messages sent to the associated number.
    incoming_text_url              URL for receiving SMS messages to the associated phone number. *Max. length:* 256 characters.
    incoming_text_method           HTTP method used for the ``incoming_text_url`` requests. *Max. length:* 8 characters. *Possible values:* ``GET`` or ``POST``. *Default value:* POST.
    incoming_text_fallback_url     URL for receiving SMS messages if ``incoming_text_url`` fails. Only valid if you provide a value for the ``incoming_text_url`` parameter. *Max. length:* 256 characters.
    incoming_text_fallback_method  HTTP method used for ``incoming_text_fallback_url`` requests. *Max. length:* 8 characters. *Possible values:* ``GET`` or ``POST``. *Default value:* POST.
    capabilities                   Set of boolean flags indicating the capabilities supported by the associated phone number.     
    city                           City where the available phone number is located.
    region                         Two-letter US state abbreviation where the available phone number is located.
    lata                           Local address and transport area (LATA) where the available phone number is located.
    rate_center                    LATA rate center where the available phone number is located. Usually the same as city.
    =============================  ===========

    Example request to retrieve a list of associated numbers::

        from vivialconnect import Resource, Number

        Resource.api_key = ""
        Resource.api_secret = ""
        Resource.api_account_id = "12345"

        def list_associated_numbers():
            numbers = Number.find()
            for number in numbers:
                print(number.id, number.name,
                      number.phone_number_type,
                      number.phone_number)

        list_associated_numbers()


    Example request to retrieve a list of available numbers::

        from vivialconnect import Resource, Number

        Resource.api_key = ""
        Resource.api_secret = ""
        Resource.api_account_id = "12345"

        def list_available_numbers(country_code='US',
                                   number_type='local',
                                   area_code='913',
                                   in_postal_code=None,
                                   in_region=None,
                                   limit=5):
            numbers = Number.available(
                country_code=country_code,
                number_type=number_type,
                area_code=area_code,
                in_postal_code=in_postal_code,
                in_region=in_region,
                limit=limit)
            for number in numbers:
                print(number.name,
                      number.phone_number_type,
                      number.phone_number)

        list_available_numbers()

    Example request to buy a new phone number::

        from vivialconnect import Resource, Number

        Resource.api_key = ""
        Resource.api_secret = ""
        Resource.api_account_id = "12345"

        def buy_number(name=None,
                       phone_number=None,
                       area_code=None,
                       phone_number_type='local'):
            number = Number()
            number.name = name
            number.phone_number = phone_number
            number.area_code = area_code
            number.phone_number_type = phone_number_type
            number.buy()

        buy_number(name='(913) 259-7591',
                   phone_number='+19132597591',
                   area_code='913',
                   phone_number_type='local')
    """

    @classmethod
    def available(cls, opts=None, **kwargs):
        """Lists available phone numbers.

        :param opts: Additional query params.
        :type opts: ``dict``.
        :param \**kwargs: You must specify exactly one of the following three keys:
            in_region, area_code, in_postal_code.

        :returns: :class:`Number` -- a list of available US local or toll-free phone numbers.
        """
        qs = {}
        country_code = "US"
        number_type = "local"
        if opts is None:
            opts = kwargs
        for k in opts.keys():
            if k == "country_code" and opts[k]:
                country_code = opts[k].upper()
            elif k == "number_type" and opts[k]:
                number_type = opts[k].lower()
            else:
                if opts[k]:
                    qs[k] = opts[k]
        url = cls._custom_path(
            custom_path="/available/{}/{}".format(country_code, number_type)
        )
        return cls._build_list(Number.request.get(url, qs))

    def buy(self):
        """Purchases a new phone number.
        """
        if self.id:
            self.id = None
        return self.save()

    def buy_local(self):
        """Purchases a new local phone number.
        """
        self.phone_number_type = "local"
        return self.save()

    def remove_tag(self, key):
        """
            Delete a tag from server
        """
        if key not in self.tags:
            raise ValueError(f"Tag with key '{key}' does not exist")
        payload = {"tags": {key: ""}}
        response = self.klass.request.delete(
            self._item_sub_resource_path(self.id, self._plural, "tags"), payload=payload
        )
        if "phone_number" in response:
            self.tags = response["phone_number"]["tags"]
            return True
        return False

    @classmethod
    def tagged_numbers(cls, **options):
        """
            Retrieve all tagged numbers from account
        """
        url = cls._custom_path(custom_path="/tags")
        # Format values of `contains` and `notcontains` query params to match the format expected by the API
        options = Util.format_filter_tag_params(options)
        return cls._build_list_from_pagination(Number.request.get(url, options))

    @classmethod
    def lookup(cls, phone_number):
        """
            Allow to get information about the device type and carrier that is associated with a specific phone number.
        """
        params = {"phone_number": phone_number}
        url = cls._custom_path(custom_path="/lookup")
        response = cls.request.get(url, params)
        return NumberInfo(attributes=response["number_info"])


Number._singular = "phone_number"
