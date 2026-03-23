from flask import Blueprint, request, jsonify
from .eels_database import EelData, EelDBManager
import os

eelsdb_blueprint = Blueprint('eels_api', __name__)
eelsdb_manager = EelDBManager(os.path.join('database', 'eelytics.db'))

@eelsdb_blueprint.route('/save_batch',  methods=['POST'])
def save_batch():
    data = request.get_json()
    return jsonify({'batch_logs': data.get('batch_logs')}), 200