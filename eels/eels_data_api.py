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

@eelsdb_blueprint.route('/get_data', methods=['GET'])
def get_avg():
    count = len(eelsdb_manager.show_data())
    elver_data = [size['size'] for size in eelsdb_manager.get_average('ELVER')]
    kuroko_data = [size['size'] for size in eelsdb_manager.get_average('KUROKO')]
    table_data = [size['size'] for size in eelsdb_manager.get_average('TABLE')]
    avg_elver = sum(elver_data) / len(elver_data)
    avg_kuroko = sum(kuroko_data) / len(kuroko_data)
    avg_table = sum(table_data) / len(table_data)
    return jsonify({
        'count': count,
        'avg_elver': avg_elver,
        'avg_kuroko': avg_kuroko,
        'avg_table': avg_table
    })
    
