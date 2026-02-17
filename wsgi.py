from flask import Flask, render_template
from accounts.accounts_api import accounts_blueprint
from model_data_transfer.mdt_api import mdt_blueprint


app = Flask(__name__)

@app.route('/api/home')
def homepage():
    return render_template('index.html')

@app.route('/api/yna')
def easter_egg():
    return render_template('yna.html')

app.register_blueprint(accounts_blueprint, url_prefix='/api/accounts')
app.register_blueprint(mdt_blueprint, url_prefix='/api/mdt')
if __name__ == '__main__':
    pass