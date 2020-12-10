import json

from tests.common import BaseTestCase, HTTMock
from vivialconnect import User, Resource
from vivialconnect.common.error import ResourceNotFound


class UserTest(BaseTestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        Resource._api_account_id = 5
        attributes = self.load_fixture("user/user")
        attributes = json.loads(attributes)
        self.user = User(attributes=attributes["user"])

    def test_create_credential(self):

        with HTTMock(
            self.response_content,
            body=self.load_fixture("user/new_credential"),
            headers={"Content-type": "application/json"},
        ):
            new_credentials = self.user.create_credential(name="Test credential")

            assert new_credentials is not None
            assert new_credentials.api_key == "MTKMYAPIKEYMYAPIKEYMYAPIKEYMYAPIKE3"
            assert (
                new_credentials.api_secret
                == "My4P1s3cr37k3yMy4P1s3cr37k3yMy4P1s3cr37k3y313371"
            )
            assert new_credentials.name == "Test credential"

    def test_get_all_credentials(self):

        with HTTMock(
            self.response_content,
            body=self.load_fixture("user/credentials"),
            headers={"Content-type": "application/json"},
        ):
            credentials = self.user.get_credentials()

            assert credentials is not None
            assert len(credentials) > 0

    def test_update_credentials(self):

        # Get all users credentials first
        with HTTMock(
            self.response_content,
            body=self.load_fixture("user/credentials"),
            headers={"Content-type": "application/json"},
        ):
            credentials = self.user.get_credentials()

        # Select a credential for the list and update it
        with HTTMock(
            self.response_content,
            body=self.load_fixture("user/update_credential"),
            headers={"Content-type": "application/json"},
        ):
            credential = credentials[0]
            credential_id = credential.id
            credential.name = "Test"
            credential.save()

            credential = self.user.get_credentials(id_=credential_id)
            assert credential.name == "Test"

    def test_count_credentials(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("user/credentials_count"),
            headers={"Content-type": "application/json"},
        ):
            credentials_count = self.user.count_credentials()

            assert credentials_count == 8

    def test_delete_credentials(self):

        # Fetch users credentials and delete the credential
        with HTTMock(
            self.response_content,
            body=self.load_fixture("user/credentials"),
            headers={"Content-type": "application/json"},
        ):
            credentials = self.user.get_credentials()
            to_delete = credentials[0]
            to_delete_id = to_delete.id
            to_delete.destroy()

        # Try to search the deleted credential, just confirming it does not exist anymore
        with HTTMock(
            self.response_content,
            headers={"Content-type": "application/json"},
            code=404,
            body={"message": f"Resource not found for credential id {to_delete_id}"},
        ), self.assertRaises(ResourceNotFound):
            self.user.get_credentials(id_=to_delete_id)
