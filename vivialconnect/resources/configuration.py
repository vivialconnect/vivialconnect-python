"""
.. module:: configuration
   :synopsis: Configuration module.
"""

from vivialconnect.resources.resource import Resource
from vivialconnect.resources.countable import Countable


class Configuration(Resource, Countable):
    """Use the Configuration resource to list, view, update, and manage
    callback configurations for your account.

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
