from flask import Blueprint, request, jsonify
from . import account_database

accounts_blueprint = Blueprint("accounts_api", __name__)

@accounts_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    username = data['username']
    password = data['password']
    
    user_cred = account_database.get_account_cred(username)
    if password == user_cred['password']:
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "user": {
                "id": user_cred['id'],
                "username": user_cred['username'],
                "email": user_cred['email'],
            }}), 200
        
    else:
        return jsonify({"status": "error", "message": "Invalid password"}), 401
