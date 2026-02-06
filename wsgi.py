from flask import Flask, render_template, jsonify
from accounts.accounts_api import accounts_blueprint
from accounts.account_database import get_db

app = Flask(__name__)

@app.route('/api/home')
def homepage():
    return render_template('index.html')

@app.route('/api/yna')
def easter_egg():
    return render_template('yna.html')

app.register_blueprint(accounts_blueprint, url_prefix='/api/accounts')
if __name__ == '__main__':
    pass