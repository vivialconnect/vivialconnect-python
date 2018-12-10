import json
import vivialconnect

from tests.common import BaseTestCase, HTTMock


class ConnectorTest(BaseTestCase):
    def test_create_connector(self):
        with HTTMock(self.response_content,
                     body=self.load_fixture('connector/connector'),
                     headers={'Content-type': 'application/json'}):
            connector = vivialconnect.Connector({'id': 424242, 'name': 'TestConnector'})
            connector.save()
        self.assertEqual(424242, connector.id)
        self.assertEqual("TestConnector", connector.name)

    def test_get_connector(self):
        with HTTMock(self.response_content,
                     body=self.load_fixture("connector/connector"),
                     headers={'Content-type': 'application/json'}):
            connector = vivialconnect.Connector.find(424242)
        self.assertEqual(424242, connector.id)
        self.assertEqual(True, connector.active)
        self.assertEqual("TestConnector", connector.name)

    def test_get_connectors(self):
        with HTTMock(self.response_content,
                     body=self.load_fixture('connector/connectors'),
                     headers={'Content-type': 'application/json'}):
            connectors = vivialconnect.Connector.find()
        self.assertEqual(2, len(connectors))

    def test_parse_callback(self):
        fixture = self.load_fixture('connector/connector_with_callback')
        cb_data = self.get_path(json.loads(fixture.decode()), 'connector.callbacks.0')
        with HTTMock(self.response_content,
                     body=fixture,
                     headers={'Content-type': 'application/json'}):
            connector = vivialconnect.Connector.find(424242)
        self.assertEqual(1, len(connector.callbacks))
        self.assertIsInstance(connector.callbacks[0], vivialconnect.ConnectorCallback)
        self.validate_with_dict(connector.callbacks[0], cb_data)

    def test_parse_phone_number(self):
        fixture = self.load_fixture('connector/connector_with_phone_number')
        phone_data = self.get_path(json.loads(fixture.decode()), 'connector.phone_numbers.0')
        with HTTMock(self.response_content,
                     body=fixture,
                     headers={'Content-type': 'application/json'}):
            connector = vivialconnect.Connector.find(424242)
        self.assertEqual(1, len(connector.phone_numbers))
        self.assertIsInstance(connector.phone_numbers[0], vivialconnect.ConnectorNumber)
        self.validate_with_dict(connector.phone_numbers[0], phone_data)

    def test_modifications(self):
        fixture = self.load_fixture('connector/connectors')
        fixture_data = json.loads(fixture.decode())
        p1_numbers = self.get_path(fixture_data, 'connectors.0.phone_numbers')
        p2_numbers = self.get_path(fixture_data, 'connectors.1.phone_numbers')
        with HTTMock(self.response_content,
                     body=fixture,
                     headers={'Content-type': 'application/json'}):
            connectors = vivialconnect.Connector.find()
            self.assertEqual(len(connectors), 2)
            c1 = connectors[0]
            c2 = connectors[1]

        self.assertSequenceEqual([p.attributes for p in c1.phone_numbers], p1_numbers)
        self.assertSequenceEqual([p.attributes for p in c2.phone_numbers], p2_numbers)

        num = c1.phone_numbers[0]
        del c1.phone_numbers[0]
        del c2.phone_numbers[1]
        self.assertSequenceEqual([p.attributes for p in c1.phone_numbers], p1_numbers[1:])
        self.assertSequenceEqual([p.attributes for p in c2.phone_numbers], p2_numbers[:1])
        c1.name = "Some Other name"
        c2.name = "Another different name"
        c1.phone_numbers.insert(0, num)
        self.assertSequenceEqual([p.attributes for p in c1.phone_numbers], p1_numbers)
        self.assertSequenceEqual([p.attributes for p in c2.phone_numbers], p2_numbers[:1])

    def test_resurrection(self):
        fixture = self.load_fixture('connector/connector_with_phone_number')
        phone_data = self.get_path(json.loads(fixture.decode()), 'connector.phone_numbers.0')
        with HTTMock(self.response_content,
                     body=fixture,
                     headers={'Content-type': 'application/json'}):
            connector = vivialconnect.Connector.find(424242)
        connector.phone_numbers.append(phone_data)
        connector.name = 'Some other name'
        connector.phone_numbers.append(phone_data)
        self.assertEqual(3, len(connector.phone_numbers))
        with HTTMock(self.response_content,
                     body=fixture,
                     headers={'Content-type': 'application/json'}):
            connector = vivialconnect.Connector.find(424242)
        self.assertEqual(1, len(connector.phone_numbers))

    def validate_with_dict(self, obj, data):
        for k, v in data.items():
            self.assertEqual(v, getattr(obj, k))

    @staticmethod
    def get_path(data, path):
        attrs = path.split('.')
        cur = data
        for attr in attrs:
            if isinstance(cur, dict):
                cur = cur[attr]
            elif isinstance(cur, list):
                cur = cur[int(attr)]
        return cur
