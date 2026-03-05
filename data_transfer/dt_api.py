from flask import Blueprint, jsonify, request
import redis
import json

dt_blueprint = Blueprint("dt_api", __name__)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@dt_blueprint.route('/live_eel', methods=['GET'])
def live_eel_data():
    raw_data = r.get('latest_eel')
    if raw_data:
        return jsonify(json.loads(raw_data))
    return jsonify({"size": 0, "group": "NONE"})

@dt_blueprint.route('/update_eel', methods=['POST'])
def update_eel_data():
    data = request.json
    r.set('latest_eel', json.dumps(data), ex=3)
    return jsonify({'status':'updated'}), 200

@dt_blueprint.route('/live_tank', methods=['GET'])
def live_tank_status():
    raw_data = r.get('latest_tank_stat')
    if raw_data:
        return jsonify(json.loads(raw_data))
    return jsonify({"water_level": 0, "action": 'NONE'})

@dt_blueprint.route('/live_tank_options', methods=['GET'])
def live_tank_options():
    raw_data = r.get('latest_tank_opt')
    if raw_data:
        return jsonify(json.loads(raw_data))
    return jsonify({"mode": 'NONE', "maintain": 0})

@dt_blueprint.route('/update_tank_options', methods=['POST'])
def update_tank_opts():
    data = request.json
    r.set('latest_tank_opt', json.dumps(data))
    return jsonify({'status':'updated'}), 200

@dt_blueprint.route('/live_tank_all', methods=['GET'])
def live_all():
    raw_stat = r.get('latest_tank_stat')
    raw_opts = r.get('latest_tank_opt')
    
    stats = json.loads(raw_stat) if raw_stat else {"water_level": 0, "action": 'NONE'}
    opts = json.loads(raw_opts) if raw_opts else {"mode": 'NONE', "maintain": 0}
    
    return jsonify({
        'status': stats,
        'opts': opts 
    })