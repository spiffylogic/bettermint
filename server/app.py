import datetime, json

from flask import abort, Flask, jsonify, request
from flask_cors import CORS

from plaid import ApiException
# from plaid.model.payment_amount import PaymentAmount
# from plaid.model.payment_amount_currency import PaymentAmountCurrency
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

# Local imports
from model import *
from plaid_setup import plaid_client, plaid_country_codes, plaid_products

from data.users import save_user
from data.accounts import get_accounts, save_account
from data.users import save_access_token
from data.transactions import *

app = Flask(__name__)
CORS(app)

import routes.transactions, routes.categories

# Create Plaid Link token
@app.route('/create_link_token', methods=['POST'])
def create_link_token():
    try:
        create_request = LinkTokenCreateRequest(
            products = plaid_products,
            client_name = "Bettermint",
            country_codes = plaid_country_codes,
            language = 'en',
            user = LinkTokenCreateRequestUser(
                client_user_id = str(datetime.datetime.now().timestamp())
            )
        )
        response = plaid_client.link_token_create(create_request)
        return jsonify(response.to_dict())
    except ApiException as e:
        return json.loads(e.body)

# Exchange token flow - exchange a Link public_token for an API access_token
# and save it for this user.
# https://plaid.com/docs/#exchange-token-flow
@app.route('/set_access_token', methods=['POST'])
def set_access_token():
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
        # Don't send access_token to client, save it in db.
        save_access_token(user_id, access_token, item_id)
        return jsonify("YAY")
    except ApiException as e:
        return json.loads(e.body)

# Manage users.
@app.route('/users/<user_id>', methods = ['GET', 'POST', 'DELETE'])
def user(user_id):
    if request.method == 'GET':
        # TODO: return the information for <user_id>
        return '{{}}'
    if request.method == 'POST':
        # modify/update the information for <user_id>
        # data = request.form # a multidict containing POST data
        if not save_user(user_id, request.json['identifier'], request.json['display_name']):
            abort(500) # Something went wrong
        return '{{}}'
    if request.method == 'DELETE':
        # TODO: delete user with ID <user_id>
        return '{{}}'
    else:
        # POST Error 405 Method Not Allowed
        abort(405)

# Manage accounts.
@app.route('/accounts', methods = ['GET', 'POST'])
def accounts():
    user_id = request.args.get('user_id')

    if request.method == 'GET':
        # Return the list of accounts for <user_id>
        return get_accounts(user_id)

    if request.method == 'POST':
        # Determine if it is a single account or list of accounts
        account = request.json.get('account')
        if account:
            save_account(account.get('id'), user_id, account.get('name'), account.get('number'))
            return '{{}}'
        accounts = request.json.get('accounts')
        if accounts:
            for account in accounts:
                # TODO: add all accounts in a single SQL query
                save_account(account.get('id'), user_id, account.get('name'), account.get('number'))
        return '{{}}'
    else:
        # POST Error 405 Method Not Allowed
        abort(405)
