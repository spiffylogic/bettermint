from flask import abort, Flask, jsonify, request
from flask_cors import CORS
import json, os, time
import mysql.connector

import plaid
# from plaid.model.payment_amount import PaymentAmount
# from plaid.model.payment_amount_currency import PaymentAmountCurrency
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
# from plaid.model.recipient_bacs_nullable import RecipientBACSNullable
# from plaid.model.payment_initiation_address import PaymentInitiationAddress
# from plaid.model.payment_initiation_recipient_create_request import PaymentInitiationRecipientCreateRequest
# from plaid.model.payment_initiation_payment_create_request import PaymentInitiationPaymentCreateRequest
# from plaid.model.payment_initiation_payment_get_request import PaymentInitiationPaymentGetRequest
# from plaid.model.link_token_create_request_payment_initiation import LinkTokenCreateRequestPaymentInitiation
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
# from plaid.model.asset_report_create_request import AssetReportCreateRequest
# from plaid.model.asset_report_create_request_options import AssetReportCreateRequestOptions
# from plaid.model.asset_report_user import AssetReportUser
# from plaid.model.asset_report_get_request import AssetReportGetRequest
# from plaid.model.asset_report_pdf_get_request import AssetReportPDFGetRequest
# from plaid.model.auth_get_request import AuthGetRequest
# from plaid.model.transactions_sync_request import TransactionsSyncRequest
# from plaid.model.identity_get_request import IdentityGetRequest
# from plaid.model.investments_transactions_get_request_options import InvestmentsTransactionsGetRequestOptions
# from plaid.model.investments_transactions_get_request import InvestmentsTransactionsGetRequest
# from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
# from plaid.model.accounts_get_request import AccountsGetRequest
# from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest
# from plaid.model.item_get_request import ItemGetRequest
# from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest
# from plaid.model.transfer_authorization_create_request import TransferAuthorizationCreateRequest
# from plaid.model.transfer_create_request import TransferCreateRequest
# from plaid.model.transfer_get_request import TransferGetRequest
# from plaid.model.transfer_network import TransferNetwork
# from plaid.model.transfer_type import TransferType
# from plaid.model.transfer_authorization_user_in_request import TransferAuthorizationUserInRequest
# from plaid.model.ach_class import ACHClass
# from plaid.model.transfer_create_idempotency_key import TransferCreateIdempotencyKey
# from plaid.model.transfer_user_address_in_request import TransferUserAddressInRequest
from plaid.api import plaid_api

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

products = []
for product in PLAID_PRODUCTS:
    products.append(Products(product))

app = Flask(__name__)
CORS(app)

mysql_config = {
  'user': 'money-user',
  'password': 'money-password',
  'host': 'localhost',
  'database': 'money',
  'raise_on_warnings': True
}

# Create Plaid Link token
@app.route('/create_link_token', methods=['POST'])
def create_link_token():
    try:
        request = LinkTokenCreateRequest(
            products=products,
            client_name="Bettermint",
            country_codes=list(map(lambda x: CountryCode(x), PLAID_COUNTRY_CODES)),
            language='en',
            user=LinkTokenCreateRequestUser(
                client_user_id=str(time.time())
            )
        )
        response = plaid_client.link_token_create(request)
        return jsonify(response.to_dict())
    except plaid.ApiException as e:
        return json.loads(e.body)

# Exchange token flow - exchange a Link public_token for an API access_token
# and save it for this user.
# https://plaid.com/docs/#exchange-token-flow
@app.route('/set_access_token', methods=['POST'])
def get_access_token():
    global access_token
    global item_id
    public_token = request.json['public_token']
    user_id = request.json['user_id']
    try:
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=public_token)
        exchange_response = plaid_client.item_public_token_exchange(exchange_request)
        access_token = exchange_response['access_token']
        item_id = exchange_response['item_id']
        print('Got {}\'s access token {}'.format(user_id, access_token))
        # don't actually send access_token to client
        # instead put it in a database, tie to authenticated user.
        # TODO: save to db!
        # HOW TO DETERMINE AUTHENTICATED USER?
        return jsonify("YAY")
    except plaid.ApiException as e:
        return json.loads(e.body)

@app.route('/users/<user_id>', methods = ['GET', 'POST', 'DELETE'])
def user(user_id):
  if request.method == 'GET':
    # TODO: return the information for <user_id>
    return '{{}}'
  if request.method == 'POST':
    # modify/update the information for <user_id>
    # data = request.form # a multidict containing POST data
    if not upsert(user_id, request.json['identifier'], request.json['display_name']):
      abort(500) # Something went wrong
    return '{{}}'
  if request.method == 'DELETE':
    # TODO: delete user with ID <user_id>
    return '{{}}'
  else:
    # POST Error 405 Method Not Allowed
    abort(405)

def upsert(user_id, identifier, display_name) -> bool:
  try:
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    sql_statement = ("REPLACE INTO users "
                  "(uid, identifier, display_name) "
                  "VALUES (%s, %s, %s)")
    sql_data = (user_id, identifier, display_name)
    cursor.execute(sql_statement, sql_data)
    connection.commit()
    cursor.close()
    connection.close()
    return True
  except mysql.connector.Error as err:
    if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
      print("Access to DB denied")
    elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
      print("Bad DB")
    else:
      print(err)
  return False
