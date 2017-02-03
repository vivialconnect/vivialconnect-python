import vivialconnect

from tests.common import BaseTestCase
from tests.common import HTTMock

class AccountTest(BaseTestCase):

    def test_get_account(self):
        with HTTMock(self.response_content,
                     body=self.load_fixture('account/account'),
                     headers={'Content-type': 'application/json'}):
            account = vivialconnect.Account.find(6242736)
        self.assertEqual("Vivial Connect", account.company_name)

    def test_update_account(self):
        with HTTMock(self.response_content,
                     body=self.load_fixture('account/account'),
                     headers={'Content-type': 'application/json'}):
            account = vivialconnect.Account.find(6242736)
        with HTTMock(self.response_content,
                     body=self.load_fixture('account/account'),
                     headers={'Content-type': 'application/json'}):
            account.save()

    def test_get_accounts(self):
        with HTTMock(self.response_content,
                     body=self.load_fixture('account/accounts'),
                     headers={'Content-type': 'application/json'}):
            accounts = vivialconnect.Account.find()
        self.assertEqual(3, len(accounts))

    def test_count_accounts(self):
        with HTTMock(self.response_content,
                     body=self.load_fixture('account/count'),
                     headers={'Content-type': 'application/json'}):
            count = vivialconnect.Account.count()
        self.assertEqual(3, count)

if __name__ == '__main__':
    unittest.main()
