import vivialconnect

from tests.common import BaseTestCase
from tests.common import HTTMock

class MessageTest(BaseTestCase):

    def test_create_message(self):
        with HTTMock(self.response_content,
                     body=self.load_fixture('message/message'),
                     headers={'Content-type': 'application/json'}):
            message = vivialconnect.Message({'id': 6242736})
            message.save()
        self.assertEqual("This is message", message.body)

    def test_get_message(self):
        with HTTMock(self.response_content,
                     body=self.load_fixture('message/message'),
                     headers={'Content-type': 'application/json'}):
            message = vivialconnect.Message.find(6242736)

        self.assertEqual("This is message", message.body)
        self.assertEqual("received", message.status)
        self.assertEqual("inbound", message.direction)
        self.assertEqual("+12223334444", message.from_number)
        self.assertEqual("+12223335555", message.to_number)
        self.assertEqual(0, message.num_media)

    def test_update_message(self):
        with HTTMock(self.response_content,
                     body=self.load_fixture('message/message'),
                     headers={'Content-type': 'application/json'}):
            message = vivialconnect.Message.find(6242736)
        with HTTMock(self.response_content,
                     body=self.load_fixture('message/message'),
                     headers={'Content-type': 'application/json'}):
            message.save()

    def test_get_messages(self):
        with HTTMock(self.response_content,
                     body=self.load_fixture('message/messages'),
                     headers={'Content-type': 'application/json'}):
            messages = vivialconnect.Message.find()
        self.assertEqual(2, len(messages))

    def test_count_messages(self):
        with HTTMock(self.response_content,
                     body=self.load_fixture('message/count'),
                     headers={'Content-type': 'application/json'}):
            count = vivialconnect.Message.count()
        self.assertEqual(2, count)

    def test_create_attachment(self):
        with HTTMock(self.response_content,
                     body=self.load_fixture('message/attachment'),
                     headers={'Content-type': 'application/json'}):
            attachment = vivialconnect.Attachment(6242737)
            attachment.size = 1024
            attachment.content_type = 'image/gif'
            attachment.file_name = 'what.gif'
            attachment.key_name = 'abcdee'
            attachment.save()

    def test_get_attachment(self):
        with HTTMock(self.response_content,
                     body=self.load_fixture('message/message'),
                     headers={'Content-type': 'application/json'}):
            message = vivialconnect.Message.find(6242736)

        with HTTMock(self.response_content,
                     body=self.load_fixture('message/attachment'),
                     headers={'Content-type': 'application/json'}):
            attachment = message.attachment(6242737)

        self.assertEqual("image/gif", attachment.content_type)
        self.assertEqual(1024, attachment.size)
        self.assertEqual("what.gif", attachment.file_name)
        self.assertEqual("abcdee", attachment.key_name)
        self.assertEqual(6242737, attachment.message_id)

    def test_update_attachment(self):
        with HTTMock(self.response_content,
                     body=self.load_fixture('message/message'),
                     headers={'Content-type': 'application/json'}):
            message = vivialconnect.Message.find(6242736)

        with HTTMock(self.response_content,
                     body=self.load_fixture('message/attachment'),
                     headers={'Content-type': 'application/json'}):
            attachment = message.attachment(6242737)
        with HTTMock(self.response_content,
                     body=self.load_fixture('message/attachment'),
                     headers={'Content-type': 'application/json'}):
            attachment.save()

    def test_get_attachments(self):
        with HTTMock(self.response_content,
                     body=self.load_fixture('message/message'),
                     headers={'Content-type': 'application/json'}):
            message = vivialconnect.Message.find(6242736)
        with HTTMock(self.response_content,
                     body=self.load_fixture('message/attachments'),
                     headers={'Content-type': 'application/json'}):
            attachments = message.attachments()
        self.assertEqual(2, len(attachments))

    def test_count_attachments(self):
        with HTTMock(self.response_content,
                     body=self.load_fixture('message/message'),
                     headers={'Content-type': 'application/json'}):
            message = vivialconnect.Message.find(6242736)
        with HTTMock(self.response_content,
                     body=self.load_fixture('message/attachments_count'),
                     headers={'Content-type': 'application/json'}):
            count = message.attachments_count()
        self.assertEqual(2, count)

if __name__ == '__main__':
    unittest.main()
