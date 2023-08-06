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
    records = db.all()
    if not records:
        abort(400, description='No records!')
    records_sorted = sorted(records, key=lambda x: x['date'])
    return jsonify(records_sorted)


# GET /balance-history/latest
@service.route('/balance-history/latest', methods=['GET'])
def get_balance_history_latest():
    """
    Get the latest record from balance history.
    """
    records = db.all()
    if not records:
        abort(400, description='No records!')
    latest = sorted(records, key=lambda x: x['date'], reverse=True)[0]
    return jsonify(latest)


# POST /balance-history
@service.route('/balance-history', methods=['POST'])
def update_balance_history():
    """
    Update balance history.
    """
    data = json.loads(request.data)
    if not data:
        abort(400, description='Request data missing!')
    db.upsert(data, where('date') == data['date'])
    return jsonify(data)


# DELETE /balance-history
@service.route('/balance-history', methods=['DELETE'])
def delete_balance_history():
    """
    Delete balance history.
    """
    db.truncate()
    return jsonify(db.all())


# Error handler 400 Bad Request
@service.errorhandler(400)
def handle_error_400(e):
    return jsonify(error=str(e)), 400


# main
if __name__ == '__main__':
    service.run()
