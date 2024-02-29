from app import app
from data.categories import *

from flask import abort, request

@app.route('/categories', methods = ['GET', 'POST'])
def categories():
    if request.method == 'GET':
        return list_categories()
    if request.method == 'POST':
        create_category(request.json['name'])
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
