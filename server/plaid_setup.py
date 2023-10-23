import os
import plaid
from plaid.api import plaid_api
from plaid.model.country_code import CountryCode
from plaid.model.products import Products

# Fill in your Plaid API keys - https://dashboard.plaid.com/account/keys
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
# Use 'sandbox' to test with Plaid's Sandbox environment (username: user_good,
# password: pass_good)
# Use `development` to test with live users and credentials and `production`
# to go live
PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')
# PLAID_PRODUCTS is a comma-separated list of products to use when initializing
# Link. Note that this list must contain 'assets' in order for the app to be
# able to create and retrieve asset reports.
PLAID_PRODUCTS = os.getenv('PLAID_PRODUCTS', 'transactions').split(',')

# PLAID_COUNTRY_CODES is a comma-separated list of countries for which users
# will be able to select institutions from.
PLAID_COUNTRY_CODES = os.getenv('PLAID_COUNTRY_CODES', 'US').split(',')

plaid_host = plaid.Environment.Sandbox

if PLAID_ENV == 'sandbox':
    plaid_host = plaid.Environment.Sandbox
if PLAID_ENV == 'development':
    plaid_host = plaid.Environment.Development
if PLAID_ENV == 'production':
    plaid_host = plaid.Environment.Production

plaid_config = plaid.Configuration(
    host=plaid_host,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
        'plaidVersion': '2020-09-14'
    }
)

plaid_api_client = plaid.ApiClient(plaid_config)
plaid_client = plaid_api.PlaidApi(plaid_api_client)

plaid_products = []
for product in PLAID_PRODUCTS:
    plaid_products.append(Products(product))

plaid_country_codes = list(map(lambda x: CountryCode(x), PLAID_COUNTRY_CODES))