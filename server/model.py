import datetime
from dataclasses import dataclass, field
from typing import Optional

from util import snake_to_title_case

# A simple object to pass to our database functions that represents the data
# our application cares about from the Plaid transaction endpoint.
@dataclass
class SimpleTransaction:
    id: str
    user_id: str
    account_id: str
    category_id: Optional[str]
    category_name: Optional[str]
    date: datetime.date
    authorized_date: datetime.date
    name: str
    amount: float
    currency_code: str
    pending_transaction_id: Optional[str]
    note: Optional[str]
    tags: list[str] = field(default_factory=list)

    @staticmethod
    def fromPlaidTransaction(txnObj, userId):
        # Static factory method to create a SimpleTransaction object from Plaid API transaction data
        return SimpleTransaction(
            txnObj['transaction_id'], # ID
            userId,                   # UserID
            txnObj['account_id'],     # Account ID
            # CATEGORY fields:
            # - category (old)
            # - personal_finance_category -> primary, detailed, confidence_level (new)
            None, # Category ID (not known yet)
            snake_to_title_case(txnObj['personal_finance_category']['primary']), # Category
            txnObj['date'],           # Date
            txnObj.get('authorized_date'), # Authorized Date (if available)
            txnObj['merchant_name'] if 'merchant_name' in txnObj else txnObj['name'],  # Name
            txnObj['amount'],         # Amount
            txnObj['iso_currency_code'],  # Currency Code
            txnObj['pending_transaction_id'],  # Pending Transaction ID
            None, # Note
        )

    @staticmethod
    def fromSQLTransaction(txnObj):
        # Static factory method to create a SimpleTransaction object from SQL transaction data
        # Perhaps the category field shoud be the ID not the name.
        return SimpleTransaction(
            txnObj['id'],             # ID
            None,                     # UserID
            txnObj['account_id'],     # Account ID
            str(txnObj['category_id']),    # Category
            txnObj['category_name'],  # Category name
            txnObj['date'],           # Date (datetime.date)
            None, # txnObj.get('authorized_date'), # Authorized Date (if available)
            txnObj['name'],           # Name
            float(txnObj['amount']),  # Amount (convert from decimal.Decimal)
            None, # txnObj['iso_currency_code'],  # Currency Code
            None, # txnObj['pending_transaction_id']  # Pending Transaction ID
            txnObj['notes']
        )

@dataclass
class Category:
    id: str
    parent_id: Optional[str]
    name: str

    @staticmethod
    def fromSQLCategory(obj):
        return Category(str(obj['id']),
                        str(obj['parent_id']) if obj['parent_id'] else '',
                        obj['name'])
