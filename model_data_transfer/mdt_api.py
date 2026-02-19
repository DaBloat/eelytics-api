from flask import Blueprint, jsonify, request
import redis
import json

mdt_blueprint = Blueprint("mdt_api", __name__)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@mdt_blueprint.route('/live', methods=['GET'])
def live_data():
    raw_data = r.get('latest_eel')
    if raw_data:
        return(jsonify(json.loads(raw_data)))
    return jsonify({"size": 0, "group": "NONE"})

@mdt_blueprint.route('/update', methods=['POST'])
def update_data():
    data = request.json
    r.set('latest_eel', json.dumps(data))
    return jsonify({'status':'updated'}), 200

