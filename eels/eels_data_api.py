from flask import Blueprint, request, jsonify
from .eels_database import EelData, EelDBManager, format_string
import os

eelsdb_blueprint = Blueprint('eels_api', __name__)
eelsdb_manager = EelDBManager(os.path.join('database', 'eelytics.db'))

@eelsdb_blueprint.route('/save_batch',  methods=['POST'])
def save_batch():
    data = request.get_json()
    for i in data.get('batch_logs'):
        date, time, inches, group = format_string(i)
        eel = EelData(date, time, inches, group, 'imgay')
        eelsdb_manager.add_data(eel)
    return jsonify({"status":"success", "message": 'Batch saved successfuly!'}), 200