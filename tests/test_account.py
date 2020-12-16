import vivialconnect

from tests.common import BaseTestCase
from tests.common import HTTMock
from vivialconnect.resources.account import Transaction


class AccountTest(BaseTestCase):
    def test_get_account(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("account/account"),
            headers={"Content-type": "application/json"},
        ):
            account = vivialconnect.Account.find(6242736)
        self.assertEqual("Vivial Connect", account.company_name)

    def test_update_account(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("account/account"),
            headers={"Content-type": "application/json"},
        ):
            account = vivialconnect.Account.find(6242736)
        with HTTMock(
            self.response_content,
            body=self.load_fixture("account/account"),
            headers={"Content-type": "application/json"},
        ):
            account.save()

    def test_get_accounts(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("account/accounts"),
            headers={"Content-type": "application/json"},
        ):
            accounts = vivialconnect.Account.find()
        self.assertEqual(3, len(accounts))

    def test_count_accounts(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("account/count"),
            headers={"Content-type": "application/json"},
        ):
            count = vivialconnect.Account.count()
        self.assertEqual(3, count)

    def test_get_transactions(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("transaction/transactions"),
            headers={"Content-type": "application/json"},
        ):
            transactions = Transaction.find()

            assert transactions is not None
            assert len(transactions) > 0

    def test_get_transaction_by_id(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("transaction/transaction-by-id"),
            headers={"Content-type": "application/json"},
        ):
            transaction_id = 3957836
            transaction = Transaction.find(id_=transaction_id)

            assert transaction is not None
            assert transaction.id == transaction_id

    def test_get_transactions_using_dates(self):

        with HTTMock(
            self.response_content,
            body=self.load_fixture("transaction/transactions"),
            headers={"Content-type": "application/json"},
        ):
            transactions = Transaction.find(
                start_time="2019-12-14T19:00:31Z", end_time="2020-12-14T19:00:31Z"
            )

            assert transactions is not None
            assert len(transactions) > 0

    def test_get_transactions_by_type(self):

        with HTTMock(
            self.response_content,
            body=self.load_fixture("transaction/transactions-by-type"),
            headers={"Content-type": "application/json"},
        ):
            transactions = Transaction.find(transaction_type="number_purchase")
            assert transactions is not None
            assert len(transactions) > 0
            for transaction in transactions:
                assert transaction.transaction_type.startswith("number_purchase")

    def test_transactions_with_params(self):

        with HTTMock(
            self.response_content,
            body=self.load_fixture("transaction/transactions-with-params"),
            headers={"Content-type": "application/json"},
        ):
            transactions = Transaction.find(
                transaction_type="number_purchase", limit=10, page=1
            )
            assert transactions is not None
            assert len(transactions) <= 10
            for transaction in transactions:
                assert transaction.transaction_type.startswith("number_purchase")


if __name__ == "__main__":
    unittest.main()
