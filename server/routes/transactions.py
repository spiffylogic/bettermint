from app import app
from data.transactions import *
from data.users import get_plaid_items
from model import SimpleTransaction

from plaid import ApiException
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid_setup import plaid_client

import datetime, math

from flask import abort, jsonify, request
from typing import Optional
from uuid6 import uuid7

# Get transactions that we have already synced from Plaid (client refresh).
@app.route('/transactions', methods = ['GET', 'POST'])
def transactions():
    user_id = request.args.get('user_id')
    if request.method == 'GET':
        # NOTE: client uses 1-based page numbers, db uses 0-based offsets.
        page = int(request.args.get('page') or 1)
        page_size = int(request.args.get('page_size') or 10)
        query = request.args.get('q')

        # TODO: consider performance tradeoffs of fetching all rows and returning the limit
        # vs two separate queries (count(*) and select rows).
        count = get_transaction_count(user_id, query)
        total_pages = math.ceil(count / page_size)

        response = {}
        response['pagination'] = {
            'current_page': page,
            'total_pages': total_pages,
            'total_records': count
        }
        response['data'] = get_transactions(user_id,
                                            (page - 1) * page_size,
                                            page_size,
                                            query)
        return response
    if request.method == 'POST':
        transaction = SimpleTransaction(
            str(uuid7()),
            user_id,
            None, # no account for now
            None, # category ID
            None, # category name
            datetime.date.today(), # date
            None, # authorized_date
            None, # name
            request.json.get('amount'),
            None, # currency code
            None, # pending transaction ID
            request.json.get('note'),
        )
        add_transaction(transaction)
        return '{}'
    else:
        # Method Not Allowed
        abort(405)

# Manage individual transactions.
# See PUT vs POST: https://stackoverflow.com/questions/630453/what-is-the-difference-between-post-and-put-in-http
@app.route('/transactions/<transaction_id>', methods = ['GET', 'PATCH', 'DELETE'])
def transaction(transaction_id):
    if request.method == 'GET':
        return jsonify(get_transaction(transaction_id))
    if request.method == 'PATCH':
        # This method DNE?
        # d = datetime.strptime(request.json['date'], '%Y-%m-%d')
        simple_transaction = SimpleTransaction(
            transaction_id,
            request.args.get('user_id'),
            request.json.get('account_id'),
            request.json.get('category_id'),
            request.json.get('category_name'),
            None, # date
            None, # authorized_date
            request.json.get('name'),
            request.json.get('amount'),
            None, # currency code
            None, # pending transaction ID
            request.json.get('note'), # note
        )
        modify_transaction(simple_transaction)
        return '{}'
    if request.method == 'DELETE':
        delete_transaction(transaction_id)
        return '{}'
    else:
        # Method Not Allowed
        abort(405)

# Sync transactions from Plaid (server refresh).
@app.route('/transactions/sync', methods = ['POST'])
def transactions_sync():
    user_id = request.args.get('user_id')
    # 1. fetch most recent cursor from the db
    items = get_plaid_items(user_id)
    summary = [0, 0, 0]
    for item in items:
        sync_summary = sync_transactions(user_id, item['id'], item['access_token'], item['transaction_cursor'])
        if sync_summary:
            summary = [sum(x) for x in zip(summary, sync_summary)]
    return summary

def sync_transactions(user_id: str, item_id: str, access_token: str, cursor: str) -> Optional[tuple]:
    print("SYNCING TRANSACTIONS FOR {}, {}, {}".format(user_id, access_token, cursor))
    added_count, removed_count, modified_count = 0, 0, 0
    try:
        # 2. fetch all transactions since last cursor
        added, modified, removed, cursor = fetch_new_sync_data(access_token, cursor if cursor else "")

        # 3. add new transactions to our database
        for transaction in added:
            simple_transaction = SimpleTransaction.fromPlaidTransaction(transaction, user_id)
            add_transaction(simple_transaction)
            added_count += 1

        # 4. update modified transactions
        for transaction in modified:
            simple_transaction = SimpleTransaction.fromPlaidTransaction(transaction, user_id)
            modify_transaction(simple_transaction)
            modified_count += 1

        # 5. process removed transactions
        for transaction in removed:
            delete_transaction(transaction["transaction_id"])
            removed_count += 1

        # 6. save most recent cursor
        save_transaction_cursor(item_id, cursor)

        print("DONE SYNC: {}, {}, {}".format(added_count, removed_count, modified_count))
        return (added_count, removed_count, modified_count)

    except ApiException as e:
        print("SYNC ERROR {}".format(e.body))
        return None

def fetch_new_sync_data(access_token: str, initial_cursor: str) -> tuple:
    keep_going = False
    added, modified, removed, cursor = [], [], [], initial_cursor
    while True:
        request = TransactionsSyncRequest(access_token)
        request.cursor = cursor
        response = plaid_client.transactions_sync(request)
        print("Added: {}, modified: {}, removed: {}, cursor: {}".format(len(response.added), len(response.modified), len(response.removed), response.next_cursor))
        added += response.added
        modified += response.modified
        removed += response.removed
        cursor = response.next_cursor
        keep_going = response.has_more
        if not keep_going: break
    return (added, modified, removed, cursor)
