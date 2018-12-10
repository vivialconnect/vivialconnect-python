"""
.. module:: connector
   :synopsis: Connector module.
"""

from vivialconnect.resources.resource import Resource, SubordinateResource
from vivialconnect.resources.countable import Countable
from vivialconnect.common.fields import ResourceListingField


class ConnectorNumber(SubordinateResource):
    """Phone Number associated with a Connector. When creating or editing a phone number
    association, you must provide a phone_number or phone_number_id for a phone number you
    own. Currently, a phone number can only be associated with a single Connector.

    ========================== ===========
    Field                      Description
    ========================== ===========
    phone_number	       String containing the phone number.
    phone_number_id	       An integer representing the id of the PhoneNumber resource associated.
    ========================== ===========
    """

    @property
    def identity(self):
        return self.phone_number


class ConnectorCallback(SubordinateResource):
    """Callback configuration associated with a Connector.

    ========================== ===========
    Field                      Description
    ========================== ===========
    date_created               Creation date (UTC) of the connector in ISO 8601 format.
    date_modified              Last modification date (UTC) of the text connector in ISO 8601 format.
    message_type	       Message type this callback applies to. Only 'text' is supported for now
    event_type                 Event type this callback applies to. 'incoming', 'incoming_fallback', 'status'
    url                        The URL that will receive callback request.
    method                     The HTTP method which will be used for this callback.
    ========================== ===========
    """

    @property
    def identity(self):
        return "message_type: {msg_type}, event_type: {evt_type}".format(
            msg_type=self.message_type, evt_type=self.event_type
        )


class Connector(Resource, Countable):
    """Use the Connector resource to manage API activity related to connector entities.

    Connector properties

    ========================== ===========
    Field                      Description
    ========================== ===========
    id                         Unique identifier of the connector object.
    date_created               Creation date (UTC) of the connector in ISO 8601 format.
    date_modified              Last modification date (UTC) of the text connector in ISO 8601 format.
    account_id                 Unique identifier of the account with the connector.
    name                       User defined descriptive label.
    callbacks                  List of callbacks representing the callback configurations for the Connector.
    phone_numbers              List of phone numbers representing the phone numbers associated to the Connector. Max 50 listed in response.
    more_numbers	       Boolean that is true if the Connector has more than 50 associated numbers.
    ========================== ===========

    Example request to retreive a list of connectors from your account::

        from vivialconnect import Resource, Connector

        Resource.api_key = ""
        Resource.api_secret = ""
        Resource.api_account_id = "12345"

        def list_connectors():
            count = Connector.count()
            connectors = Connector.find()
            for connector in connectors:
                print(connector.id, connector.name)

        list_connectors()
    """

    phone_numbers = ResourceListingField("phone_numbers", ConnectorNumber)
    callbacks = ResourceListingField("callbacks", ConnectorCallback)
