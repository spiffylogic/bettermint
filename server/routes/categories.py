from app import app
from data.categories import *

from flask import abort, request

@app.route('/categories', methods = ['GET', 'POST'])
def categories():
    user_id = request.args.get('user_id')
    if not user_id: abort(400)
    if request.method == 'GET':
        return list_categories(user_id)
    if request.method == 'POST':
        name = request.json['name']
        if not name: abort(400)
        save_category(user_id, name)
        return ''
    else: abort(405)

@app.route('/categories/<id>', methods = ['PUT', 'DELETE'])
def category(id):
    if request.method == 'PUT':
        update_category(id, request.json['name'])
    if request.method == 'DELETE':
        delete_category(id)
    else: abort(405)
    return ''
