TEST_ACCOUNT_ID = "TEST_ACCOUNT_ID"
TEST_TRANSACTION_ID = "TEST_TRANSACTION_ID"
TEST_USER_ID = "TEST_USER_ID"
TEST_ITEM_ID = "TEST_ITEM_ID"

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
    'amount': 36.99,
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
