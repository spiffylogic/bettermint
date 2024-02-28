import data.accounts
import data.transactions
import data.users
from model import SimpleTransaction
import routes.transactions
from test_data import *

import unittest
from unittest import mock

def modified_fetch_new_sync_data(*args, **kwargs) -> tuple:
    # added, modified, removed, cursor
    return ([], [MODIFIED_TX], [], None)

def removed_fetch_new_sync_data(*args, **kwargs) -> tuple:
    # added, modified, removed, cursor
    return ([], [], [DELETED_TX], None)

class TransactionTests(unittest.TestCase):

    def setUp(self) -> None:
        # For now, use test data in the MySQL db.
        # Consider using mock database (https://medium.com/swlh/python-testing-with-a-mock-database-sql-68f676562461).
        data.users.save_user(TEST_USER_ID, "", "")
        data.accounts.save_account(TEST_ACCOUNT_ID, TEST_USER_ID, "", "")
        data.users.save_access_token(TEST_USER_ID, "", TEST_ITEM_ID)
        tx = SimpleTransaction.fromPlaidTransaction(SAMPLE_TX, TEST_USER_ID)
        data.transactions.add_transaction(tx)
        return super().setUp()

    def tearDown(self) -> None:
        # This should have a cascade deletion effect on other tables.
        data.users.delete_user(TEST_USER_ID)
        return super().tearDown()

    @mock.patch('routes.transactions.fetch_new_sync_data', side_effect = modified_fetch_new_sync_data)
    def test_sync_modified(self, mock_fetch):
        existing_tx = data.transactions.get_transaction(TEST_TRANSACTION_ID)
        summary = routes.transactions.sync_transactions(TEST_USER_ID, TEST_ITEM_ID, None, None)
        self.assertEqual(summary, (0, 0, 1))
        modified_tx = data.transactions.get_transaction(TEST_TRANSACTION_ID)
        self.assertEqual(existing_tx.amount, SAMPLE_TX['amount'])
        self.assertEqual(modified_tx.amount, MODIFIED_TX['amount'])

    @mock.patch('routes.transactions.fetch_new_sync_data', side_effect = removed_fetch_new_sync_data)
    def test_sync_deleted(self, mock_fetch):
        existing_tx = data.transactions.get_transaction(TEST_TRANSACTION_ID)
        self.assertIsNotNone(existing_tx)
        summary = routes.transactions.sync_transactions(TEST_USER_ID, TEST_ITEM_ID, None, None)
        self.assertEqual(summary, (0, 1, 0))
        deleted_tx = data.transactions.get_transaction(TEST_TRANSACTION_ID)
        self.assertIsNone(deleted_tx)

    def test_get_transaction_count(self):
        count = data.transactions.get_transaction_count(TEST_USER_ID)
        self.assertEqual(count, 1)

unittest.main()
