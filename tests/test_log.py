import vivialconnect
from tests.common import BaseTestCase, HTTMock


class LogTest(BaseTestCase):
    def test_get_logs(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("log/log"),
            headers={"Conent-type": "application/json"},
        ):
            params = {"start_time": "20181101T145548Z", "end_time": "20181205T155548Z"}
            last_key, logs = vivialconnect.Log.find(**params)
        self.assertTrue(last_key != "")
        # Check the amount of items
        self.assertTrue(isinstance(logs, list))
        self.assertEqual(len(logs), 16)

    def test_get_aggregated_logs(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("log/log_aggregated"),
            headers={"Conent-type": "application/json"},
        ):
            params = {"start_time": "20181101T145548Z", "end_time": "20181205T155548Z"}
            logs = vivialconnect.Log.get_aggregated_logs(**params)
        self.assertIn("log_items", logs)
        self.assertIn("last_key", logs)
        # Check for keys in an log item
        log_item = logs["log_items"][0]
        self.assertIn("account_id", log_item)
        self.assertIn("account_id_log_type", log_item)
        self.assertIn("log_timestamp", log_item)
        self.assertIn("aggregate_key", log_item)
        self.assertIn("log_count", log_item)
        self.assertIn("log_type", log_item)
        # Check the amount of items
        self.assertEqual(len(logs["log_items"]), 7)

    def test_get_aggregated_logs_with_log_type(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("log/log_aggregated_log_type"),
            headers={"Conent-type": "application/json"},
        ):
            params = {
                "start_time": "20181101T145548Z",
                "end_time": "20181205T155548Z",
                "optional_query_parameters": {"log_type": "user.login"},
            }
            logs = vivialconnect.Log.get_aggregated_logs(**params)
        self.assertIn("log_items", logs)
        self.assertIn("last_key", logs)
        log_item = logs["log_items"][0]
        # Check log item structure
        self.assertIn("account_id", log_item)
        self.assertIn("account_id_log_type", log_item)
        self.assertIn("log_timestamp", log_item)
        self.assertIn("aggregate_key", log_item)
        self.assertIn("log_count", log_item)
        self.assertIn("log_type", log_item)
        # Check content
        self.assertTrue("4", log_item["account_id"])
        self.assertTrue("4-user.login", log_item["account_id_log_type"])
        self.assertTrue("minutes", log_item["aggregate_key"])
        self.assertTrue(201811281404, log_item["log_timestamp"])
        self.assertTrue("user.login", log_item["log_type"])
        # Check the amount of items
        self.assertEqual(len(logs["log_items"]), 2)
