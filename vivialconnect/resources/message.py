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
        url = self.klass._custom_path(id_=self.id,
                                      custom_path="/attachments/%s" % id, options=None) + \
            self.klass._query_string(kwargs)
        attachment = Attachment._build_object(Attachment.request.get(url))
        attachment._entity_path = url
        return attachment

    def attachments(self, **kwargs):
        """Use this method to view the list of attachments for a message in
        your account.

        :param \**kwargs: Any keyword arguments used for forming a query.
        :returns: ``list`` -- a list of Resource objects.
        """
        url = self.klass._custom_path(id_=self.id, custom_path="/attachments", options=None) + \
            self.klass._query_string(kwargs)
        attachments = Attachment._build_list(Attachment.request.get(url))
        for attachment in attachments:
            attachment._entity_path = self.klass._custom_path(id_=self.id,
                                                              custom_path="/attachments/%s" % attachment.id,
                                                              options=None) + \
            self.klass._query_string(kwargs)
        return attachments

    def attachments_count(self, opts=None, **kwargs):
        """Use this method to view the total number of media attachments for
        a message in your account.
        """
        if opts is None:
            opts = kwargs

        url = self.klass._custom_path(id_=self.id, custom_path="/attachments/count", options=None) + \
            self.klass._query_string(opts)

        return Util.remove_root(Attachment.request.get(url))


class Attachment(Resource, Countable):
    """Use the :class:`Attachment` resource to list, count, and view
    information about media attachments for individual text messages in
    your account.
    """

    def __init__(self, attributes=None, prefix_options=None, message_id=None):
        self._entity_path = None
        self._message_id = message_id
        super(Attachment, self).__init__(attributes=attributes, prefix_options=prefix_options)

    def save(self, **kwargs):
        attributes = self._wrap_attributes(root=self._singular)
        if self.id:
            if not self._entity_path:
                raise ResourceError('Attachment must be loaded from associated Message')

            response = self.klass.request.put(self._entity_path, attributes)
        else:
            if not self._message_id:
                raise ResourceError('message_id must be specified when creating Attachment')

            collection_url = '/accounts/%d/messages/%d/attachments.json%s' % (int(Attachment.api_account_id),
                                                                              self._message_id,
                                                                              Attachment._query_string(kwargs))

            response = self.klass.request.post(collection_url, attributes)
        self._update(Util.remove_root(response))
        return True
