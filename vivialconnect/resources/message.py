"""
.. module:: message
   :synopsis: Message module.
"""

from vivialconnect.common.util import Util
from vivialconnect.resources.resource import Resource
from vivialconnect.resources.countable import Countable
from vivialconnect.common.error import ResourceError


class Message(Resource, Countable):
    """Use the Message resource to manage API activity related to text
    message entities.

    Message properties

    ========================== ===========
    Field                      Description                                                                                                                                     
    ========================== ===========
    id                         Unique identifier of the text message object.
    date_created               Creation date (UTC) of the text message in ISO 8601 format.
    date_modified              Last modification date (UTC) of the text message in ISO 8601 format.
    account_id                 Unique identifier of the account with the text message.
    message_type               String identifying the type of inbound or outbound text message. *Possible values:* ``local_sms``, ``tollfree_sms``, or ``local_mms``.
    direction                  Inbound/outbound direction of the text message, and if outbound, the nature of the text message initiation.
    to_number                  Phone number that received the text message. Uses E.164 format (+country code +phone number). For US, the format will be ``+1xxxyyyzzzz``.
    from_number                For inbound messages, the external phone number that sent the text message. For outbound messages, the associated phone number in your account that sent the text message.
    sent                       For inbound messages, the UTC timestamp the text message was received. For outbound messages, the UTC timestamp the text message was sent.
    body                       Text body of the text message. *Max. length:* 1,600 characters.
    num_media                  Number of media attachments for the text message.
    num_segments               Number of segments that make up the message. *Note:* Does not affect pricing.
    status                     Status of the message (for example, ``sent``).
    error_code                 Error code, if any, for the message. *Default value:* null (message was delivered successfully).
    error_message              Error code message for ``error_code`` as it is displayed to users.
    price                      Amount billed for the message, in the currency associated with the account.
    price_currency             Currency in which price is measured in ISO 4127 format. For US, the currency will be ``USD``.
    sms_configuration_id       Unique identifier of the message status callback configuration to be used to handle message status callbacks.
    ========================== ===========

    Example request to retreive a list of messages from your account::

        from vivialconnect import Resource, Message

        Resource.api_key = ""
        Resource.api_secret = ""
        Resource.api_account_id = "12345"

        def list_messages():
            count = Message.count()
            messages = Message.find()
            for message in messages:
                print(message.id, message.to_number,
                      message.from_number, message.body)

        list_messages()

    """

    def send(self):
        """Sends a new message.
        """
        return self.save()

    def attachment(self, id, **kwargs):
        """Use this method to view information about a single media attachment
        for a message in your account.

        :param id: Message id.
        :type id: ``int``.
        :returns: :class:`Resource` -- a Resource object.
        """
        url = self.klass._custom_path(
            id_=self.id, custom_path="/attachments/%s" % id, options=None
        ) + self.klass._query_string(kwargs)
        attachment = Attachment._build_object(Attachment.request.get(url))
        attachment._entity_path = url
        return attachment

    def attachments(self, **kwargs):
        """Use this method to view the list of attachments for a message in
        your account.

        :param \**kwargs: Any keyword arguments used for forming a query.
        :returns: ``list`` -- a list of Resource objects.
        """
        url = self.klass._custom_path(
            id_=self.id, custom_path="/attachments", options=None
        ) + self.klass._query_string(kwargs)
        attachments = Attachment._build_list(Attachment.request.get(url))
        for attachment in attachments:
            attachment._entity_path = self.klass._custom_path(
                id_=self.id, custom_path="/attachments/%s" % attachment.id, options=None
            ) + self.klass._query_string(kwargs)
        return attachments

    def attachments_count(self, opts=None, **kwargs):
        """Use this method to view the total number of media attachments for
        a message in your account.
        """
        if opts is None:
            opts = kwargs

        url = self.klass._custom_path(
            id_=self.id, custom_path="/attachments/count", options=None
        ) + self.klass._query_string(opts)

        return Util.remove_root(Attachment.request.get(url))


class Attachment(Resource):
    """Use the :class:`Attachment` resource to list, count, and view
    information about media attachments for individual text messages in
    your account.

    Attachment properties

    =============  ===========
    Field          Description
    =============  ===========
    id             Unique identifier of the media attachment object.
    date_created   Creation date (UTC) of the media attachment in ISO 8601 format.
    date_modified  Last modification date (UTC) of the media attachment in ISO 8601 format.
    account_id     Unique identifier of your account.
    message_id     Unique identifier of the text message for the media attachment.
    content_type   Mime-type of the media attachment.
    size           Size of the media attachment in bytes.
    file_name      File name of the media attachment.
    =============  ===========
    """

    pass
