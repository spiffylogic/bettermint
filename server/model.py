# A simple object to pass to our database functions that represents the data
# our application cares about from the Plaid transaction endpoint.

class SimpleTransaction:
  def __init__(self, id, user_id, account_id, category, date, authorized_date, name, amount, currency_code, pending_transaction_id):
    # Initialize the SimpleTransaction object with the provided data
    self.id = id
    self.user_id = user_id
    self.account_id = account_id
    self.category = category
    self.date = date
    self.authorized_date = authorized_date
    self.name = name
    self.amount = amount
    self.currency_code = currency_code
    self.pending_transaction_id = pending_transaction_id

  @staticmethod
  def fromPlaidTransaction(txnObj, userId):
    # Static factory method to create a SimpleTransaction object from Plaid API transaction data
    return SimpleTransaction(
      txnObj['transaction_id'], # ID
      userId,                   # UserID
      txnObj['account_id'],     # Account ID
      txnObj['personal_finance_category']['primary'], # Category
      txnObj['date'],           # Date
      txnObj.get('authorized_date'), # Authorized Date (if available)
      txnObj['merchant_name'] if 'merchant_name' in txnObj else txnObj['name'],  # Name
      txnObj['amount'],         # Amount
      txnObj['iso_currency_code'],  # Currency Code
      txnObj['pending_transaction_id']  # Pending Transaction ID
    )
