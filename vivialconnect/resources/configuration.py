"""
.. module:: configuration
   :synopsis: Configuration module.
"""

from vivialconnect.resources.resource import Resource
from vivialconnect.resources.countable import Countable


class Configuration(Resource, Countable):
    """Use the Configuration resource to list, view, update, and manage
    callback configurations for your account.

    Configuration properties
  
  	======================== ===========
	Field                    Description
	======================== ===========
    id                       Unique identifier of the configuration object.
    date_created             Creation date of the configuration in ISO 8601 UTC format.
    date_modified            Last modification date of the configuration in ISO 8601 UTC format.
    account_id               Unique identifier of the account or subaccount associated with the configuration.
    name                     Display name of the configuration. *Max. length:* 256 characters.
    phone_number             Associated phone number in E.164 format (+country code +phone number). For US numbers, the format will be ``+1xxxyyyzzzz``.
    phone_number_type        Type of associated phone number. *Possible values:* local (non-toll-free) or tollfree.
    message_status_callback  URL to receive message status callback requests for the associated phone number or outbound text message that specifies this configuration in its ``sms_configuration_id`` property.
    sms_url                  URL for receiving SMS messages to the associated phone number or outbound text message that specifies this configuration in its ``sms_configuration_id property.`` *Max. length:* 256 characters.
    sms_method               HTTP method used for the sms_url requests. Max. length: 8 characters. Possible values: ``GET`` or ``POST``. *Default value:* POST.              
    sms_fallback_url         URL for receiving SMS messages if ``sms_url`` fails. Only valid if you provide a value for the ``sms_url`` parameter. *Max. length:* 256 characters.
    sms_fallback_method      HTTP method used for ``sms_url_fallback`` requests. *Max. length:* 8 characters. *Possible values:* GET or POST. *Default value:* POST.
    ======================== ===========

    Example request how to create a new configuration entry::

	    from vivialconnect import Resource, Configuration

		Resource.api_key = "MY_KEY"
		Resource.api_secret = "MY_SECRET"
		Resource.api_account_id = "12345"

		def create_config(name=None,
                          phone_number=None,
                          phone_number_type=None,
                          message_status_callback=None,
                          sms_url=None,
                          sms_method=None,
                          sms_fallback_url=None,
                          sms_fallback_method=None):
		    config = Configuration()
		    config.name = name
		    config.phone_number = phone_number
		    config.phone_number_type = phone_number_type
		    config.message_status_callback = message_status_callback
		    config.sms_url = sms_url
		    config.sms_method = sms_method
		    config.sms_fallback_url = sms_fallback_url
		    config.sms_fallback_method = sms_fallback_method
		    config.save()
		    return config

		config = create_config(name='Test Configuration 1',
			                   phone_number='+19132597591',
			                   phone_number_type='local',
			                   sms_url='https://localhost/receive')
		print(config.id, config.name)
    """
    pass
