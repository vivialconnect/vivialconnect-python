import vivialconnect

from tests.common import BaseTestCase
from tests.common import HTTMock
from vivialconnect import Message


class MessageTest(BaseTestCase):
    def test_create_message(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("message/message"),
            headers={"Content-type": "application/json"},
        ):
            message = vivialconnect.Message({"id": 6242736})
            message.save()
        self.assertEqual("This is message", message.body)

    def test_get_message(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("message/message"),
            headers={"Content-type": "application/json"},
        ):
            message = vivialconnect.Message.find(6242736)

        self.assertEqual("This is message", message.body)
        self.assertEqual("received", message.status)
        self.assertEqual("inbound", message.direction)
        self.assertEqual("+12223334444", message.from_number)
        self.assertEqual("+12223335555", message.to_number)
        self.assertEqual(0, message.num_media)

    def test_update_message(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("message/message"),
            headers={"Content-type": "application/json"},
        ):
            message = vivialconnect.Message.find(6242736)
        with HTTMock(
            self.response_content,
            body=self.load_fixture("message/message"),
            headers={"Content-type": "application/json"},
        ):
            message.save()

    def test_get_messages(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("message/messages"),
            headers={"Content-type": "application/json"},
        ):
            messages = vivialconnect.Message.find()
        self.assertEqual(2, len(messages))

    def test_count_messages(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("message/count"),
            headers={"Content-type": "application/json"},
        ):
            count = vivialconnect.Message.count()
        self.assertEqual(2, count)

    def test_create_attachment(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("message/attachment"),
            headers={"Content-type": "application/json"},
        ):
            attachment = vivialconnect.Attachment(6242737)
            attachment.size = 1024
            attachment.content_type = "image/gif"
            attachment.file_name = "what.gif"
            attachment.key_name = "abcdee"
            attachment.save()

    def test_get_attachment(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("message/message"),
            headers={"Content-type": "application/json"},
        ):
            message = vivialconnect.Message.find(6242736)

        with HTTMock(
            self.response_content,
            body=self.load_fixture("message/attachment"),
            headers={"Content-type": "application/json"},
        ):
            attachment = message.attachment(6242737)

        self.assertEqual("image/gif", attachment.content_type)
        self.assertEqual(1024, attachment.size)
        self.assertEqual("what.gif", attachment.file_name)
        self.assertEqual("abcdee", attachment.key_name)
        self.assertEqual(6242737, attachment.message_id)

    def test_update_attachment(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("message/message"),
            headers={"Content-type": "application/json"},
        ):
            message = vivialconnect.Message.find(6242736)

        with HTTMock(
            self.response_content,
            body=self.load_fixture("message/attachment"),
            headers={"Content-type": "application/json"},
        ):
            attachment = message.attachment(6242737)
        with HTTMock(
            self.response_content,
            body=self.load_fixture("message/attachment"),
            headers={"Content-type": "application/json"},
        ):
            attachment.save()

    def test_get_attachments(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("message/message"),
            headers={"Content-type": "application/json"},
        ):
            message = vivialconnect.Message.find(6242736)
        with HTTMock(
            self.response_content,
            body=self.load_fixture("message/attachments"),
            headers={"Content-type": "application/json"},
        ):
            attachments = message.attachments()
        self.assertEqual(2, len(attachments))

    def test_count_attachments(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("message/message"),
            headers={"Content-type": "application/json"},
        ):
            message = vivialconnect.Message.find(6242736)
        with HTTMock(
            self.response_content,
            body=self.load_fixture("message/attachments_count"),
            headers={"Content-type": "application/json"},
        ):
            count = message.attachments_count()
        self.assertEqual(2, count)

    def test_send_bulk_message(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("message/send_bulk"),
            headers={"Content-Type": "application/json"},
        ):
            message = Message()
            message.from_number = "+16164320123"
            message.to_numbers = ["+16165444547", "+16165648990"]
            message.body = "Bulk Message Test"
            bulk_id = message.send_bulk()

            self.assertIsNotNone(bulk_id)

    def test_raise_error_without_to_numbers_property(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("message/send_bulk"),
            headers={"Content-Type": "application/json"},
        ), self.assertRaises(ValueError):
            message = Message()
            message.from_number = "+16164320123"
            message.body = "Bulk Message Test"
            message.send_bulk()

    def test_get_bulk_messages(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("message/bulk_messages"),
            headers={"Content-Type": "application/json"},
        ):
            bulk_messages = Message.bulk_messages(
                "ac84229f-86ca-5edb-a37b-df253a94dbcb"
            )
            self.assertGreater(len(bulk_messages), 0)
            message = bulk_messages[0]
            self.assertEqual(message.body, "Bulk Message Test")
            self.assertEqual(message.message_type, "local_sms")

    def test_get_all_bulks(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("message/bulks"),
            headers={"Content-Type": "application/json"},
        ):
            bulks = Message.bulks()
            self.assertGreater(len(bulks), 0)

            sample_bulk = bulks[0]

            self.assertEqual(sample_bulk.errors, 0)
            self.assertGreater(sample_bulk.total_messages, 1)
            self.assertGreater(sample_bulk.processed, 1)

    def test_send_mms_without_body(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("message/message_empty_body"),
            headers={"Content-type": "application/json"},
        ):
            message = vivialconnect.Message()
            message.from_number = "+12223334444"
            message.to_number = "12223335555"
            message.media_urls = ["http://www.sample-pic.com/sample.jpg"]
            message.save()

            self.assertTrue(hasattr(message, "body") and message.body == "")


if __name__ == "__main__":
    unittest.main()
