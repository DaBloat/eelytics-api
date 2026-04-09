from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash 
from .account_database import Account, AccountManager
import os

accounts_blueprint = Blueprint("accounts_api", __name__)
acc_db_client = AccountManager(os.path.join('database', 'eelytics.db'))

@accounts_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    user_cred = acc_db_client.get_account_cred(username)
    
    if user_cred == 0 or not check_password_hash(user_cred['password'], password):
        return jsonify({"status": "error", "message": "Invalid Username or Password"}), 401
    
    else:
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "user": {
                "id": user_cred['id'],
                "first_name": user_cred['first_name'],
                "email": user_cred['email'],
            }}), 200
    
@accounts_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    hashed_pass = generate_password_hash(data.get('pas'))
    
    new_account = Account(data.get('fn'), data.get('ln'), data.get('suf'), data.get('usr'), data.get('em'), hashed_pass, 'image.png')
    response = acc_db_client.create_account(new_account)
    if not response['status']:
        return jsonify({"status":"error", "message": 'Username or Email already exists'}), 409
    else:
        return jsonify({"status":"success", "message": 'New Account Created'}), 201
    