from flask import Blueprint, jsonify, request

mdt_blueprint = Blueprint("mdt_api", __name__)

model_data = {
    'size': 0,
    'group': 'NONE' 
}

@mdt_blueprint.route('/live', methods=['GET'])
def live_data():
    return jsonify(model_data)

@mdt_blueprint.route('/update', methods=['POST'])
def update_data():
    global model_data
    model_data = request.json
    return jsonify({'status':'updated'}), 200

