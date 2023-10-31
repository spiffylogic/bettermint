import app
import unittest
from unittest import mock
import json
import sql
from model import SimpleTransaction

# TODO: move these fake data to another file
TEST_ACCOUNT_ID = "TEST_ACCOUNT_ID"
TEST_TRANSACTION_ID = "TEST_TRANSACTION_ID"
TEST_USER_ID = "TEST_USER_ID"

SAMPLE_TX = {
  'account_id': TEST_ACCOUNT_ID,
  'account_owner': None,
  'amount': 6.33,
  'authorized_date': "2021-03-23",
  'authorized_datetime': None,
  'category': ["Travel", "Taxi"],
  'category_id': "22016000",
  'check_number': None,
  'date': "2021-03-24",
  'datetime': None,
  'iso_currency_code': "USD",
  'location': {
    'address': None,
    'city': None,
    'country': None,
    'lat': None,
    'lon': None,
    'postal_code': None,
    'region': None,
    'store_number': None,
  },
  'merchant_name': "Uber",
  'name': "Uber 072515 SF**POOL**",
  'payment_channel': "online",
  'payment_meta': {
    'by_order_of': None,
    'payee': None,
    'payer': None,
    'payment_method': None,
    'payment_processor': None,
    'ppd_id': None,
    'reason': None,
    'reference_number': None,
  },
  'pending': False,
  'pending_transaction_id': None,
  'personal_finance_category': {
    'detailed': "TRANSPORTATION_TAXIS_AND_RIDE_SHARES",
    'primary': "TRANSPORTATION",
  },
  'transaction_code': None,
  'transaction_id': TEST_TRANSACTION_ID,
  'transaction_type': "special",
  'unofficial_currency_code': None
}

MODIFIED_TX = {
  'account_id': TEST_ACCOUNT_ID,
  'account_owner': None,
  'amount': 6.33,
  'authorized_date': "2021-03-23",
  'authorized_datetime': None,
  'category': ["Travel", "Taxi"],
  'category_id': "22016000",
  'check_number': None,
  'date': "2021-03-24",
  'datetime': None,
  'iso_currency_code': "USD",
  'location': {
    'address': None,
    'city': None,
    'country': None,
    'lat': None,
    'lon': None,
    'postal_code': None,
    'region': None,
    'store_number': None,
  },
  'merchant_name': "Uber",
  'name': "Uber 072515 SF**POOL**",
  'payment_channel': "online",
  'payment_meta': {
    'by_order_of': None,
    'payee': None,
    'payer': None,
    'payment_method': None,
    'payment_processor': None,
    'ppd_id': None,
    'reason': None,
    'reference_number': None,
  },
  'pending': False,
  'pending_transaction_id': None,
  'personal_finance_category': {
    'detailed': "TRANSPORTATION_TAXIS_AND_RIDE_SHARES",
    'primary': "TRANSPORTATION",
  },
  'transaction_code': None,
  'transaction_id': TEST_TRANSACTION_ID,
  'transaction_type': "special",
  'unofficial_currency_code': None
}

DELETED_TX = {
  'transaction_id': TEST_TRANSACTION_ID,
}

def mocked_fetch_new_sync_data(*args, **kwargs) -> tuple:
  added, modified, removed, cursor = [], [MODIFIED_TX], [], None
  return (added, modified, removed, cursor)

class TransactionTests(unittest.TestCase):

  def setUp(self) -> None:
    # For now, use test data in the MySQL db.
    # TODO: use mock database (https://medium.com/swlh/python-testing-with-a-mock-database-sql-68f676562461).
    sql.upsert_user(TEST_USER_ID, "", "")
    sql.save_account(TEST_ACCOUNT_ID, TEST_USER_ID, "", "")
    tx = SimpleTransaction.fromPlaidTransaction(SAMPLE_TX, TEST_USER_ID)
    sql.delete_transaction(tx)
    sql.add_new_transaction(tx)
    return super().setUp()

  def tearDown(self) -> None:
    # This should have a cascade deletion effect on other tables.
    sql.remove_user(TEST_USER_ID)
    return super().tearDown()

  # Mock fetch_new_sync_data() to return sample data for test
  @mock.patch('app.fetch_new_sync_data', side_effect = mocked_fetch_new_sync_data)
  def test_sync_modified(self, mock_fetch):
    app.sync_transactions(TEST_USER_ID, None, None)
    # TODO: assert field(s) before and after
    pass

  def test_sync_deleted(self):
    # Check existing before and deleted after
    pass

unittest.main()