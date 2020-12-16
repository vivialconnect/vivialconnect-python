import unittest

from tests.common import HTTMock, BaseTestCase
from vivialconnect import Number


class NumberTest(BaseTestCase):
    def test_retrieve_all_tags(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("number/all_tags"),
            headers={"Content-type": "application/json"},
        ):
            tagged_numbers = Number.tagged_numbers()
            assert len(tagged_numbers) > 0

    def test_filter_tags(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("number/filter_tags"),
            headers={"Content-type": "application/json"},
        ):
            tagged_numbers = Number.tagged_numbers(contains={"category": "UPDATED"})
            tagged_number = tagged_numbers[0]

            assert "category" in tagged_number.tags
            assert "UPDATED" == tagged_number.tags["category"]

    def test_update_tags(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("number/all_tags"),
            headers={"Content-type": "application/json"},
        ):
            tagged_numbers = Number.tagged_numbers()
            tagged_number = tagged_numbers[0]
            tagged_number.tags["to_update"] = "dummy"
            tagged_number.save()

            assert "to_update" in tagged_number.tags
            assert "dummy" == tagged_number.tags["to_update"]

    def test_delete_tags(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("number/filter_tags"),
            headers={"Content-type": "application/json"},
        ):
            tagged_numbers = Number.tagged_numbers(contains={"category": "UPDATED"})
            tagged_number = tagged_numbers[0]

        with HTTMock(
            self.response_content,
            body=self.load_fixture("number/deleted_tag"),
            headers={"Content-type": "application/json"},
        ):
            r = tagged_number.remove_tag("to_delete")
            assert r is True
            assert "to_delete" not in tagged_number.tags

    def test_number_lookup(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("number/number_lookup"),
            headers={"Content-type": "application/json"},
        ):
            lookup = Number.lookup("+15152073167")

            assert lookup.phone_number.strip() == "15152073167"
            assert lookup.carrier["country"] == "US"
            assert lookup.device["model"] == "APL iPhone6"

    def test_search_available_tollfree(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("number/available-tollfree"),
            headers={"Content-type": "application/json"},
        ):
            available_numbers = Number.available(number_type="tollfree")

            for number in available_numbers:
                assert number.phone_number[2:].startswith("833")

    def test_purchase_tollfree_number(self):
        with HTTMock(
            self.response_content,
            body=self.load_fixture("number/tollfree-purchase"),
            headers={"Content-type": "application/json"},
        ):
            number = Number()
            number.phone_number = "+18332210936"
            number.phone_number_type = "tollfree"
            number.buy()

            assert number.id is not None


if __name__ == "__main__":
    unittest.main()
