import json
from flask import Flask, request, jsonify, abort
from tinydb import TinyDB, where


# init API service
service = Flask(__name__)

# init file DB
db = TinyDB('/tmp/db.json')


# GET /balance-history
@service.route('/balance-history', methods=['GET'])
def get_balance_history():
    """
    Get balance history.
    """
    date = request.args.get('date')
    if not date:
        # get all records
        return jsonify(db.all())
    else:
        # get single record by date
        r = db.search(where('date') == date)
        if r:
            return jsonify(r)
        abort(400, description='Record with such date not found!')


# POST /balance-history
@service.route('/balance-history', methods=['POST'])
def update_balance_history():
    """
    Update balance history.
    """
    data = json.loads(request.data)
    if not data:
        abort(400, description='Request data is missing!')
    db.upsert(data, where('date') == data['date'])
    return jsonify(data)


# DELETE /balance-history
@service.route('/balance-history', methods=['DELETE'])
def delete_balance_history():
    """
    Delete balance history.
    """
    db.truncate()
    return db.all()


# Error handler 400 Bad Request
@service.errorhandler(400)
def error_handler_400(e):
    return jsonify(error=str(e)), 400


# main
if __name__ == '__main__':
    service.run()
