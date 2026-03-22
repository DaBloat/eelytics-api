from flask import Flask, render_template
from accounts.accounts_api import accounts_blueprint
from data_transfer.dt_api import dt_blueprint
from eels.eels_data_api import eelsdb_blueprint


app = Flask(__name__)

@app.route('/api/home')
def homepage():
    return render_template('index.html')

@app.route('/api/yna')
def easter_egg():
    return render_template('yna.html')

app.register_blueprint(accounts_blueprint, url_prefix='/api/accounts')
app.register_blueprint(dt_blueprint, url_prefix='/api/dt')
app.register_blueprint(eelsdb_blueprint, url_prefix='/api/eelsdb')
if __name__ == '__main__':
    pass