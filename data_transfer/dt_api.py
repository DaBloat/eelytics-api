from flask import Blueprint, jsonify, request
import redis
import json

dt_blueprint = Blueprint("dt_api", __name__)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@dt_blueprint.route('/live_eel', methods=['GET'])
def live_eel_data():
    raw_data = r.get('latest_eel')
    if raw_data:
        return(jsonify(json.loads(raw_data)))
    return jsonify({"size": 0, "group": "NONE"})

@dt_blueprint.route('/update_eel', methods=['POST'])
def update_eel_data():
    data = request.json
    r.set('latest_eel', json.dumps(data), ex=3)
    return jsonify({'status':'updated'}), 200

