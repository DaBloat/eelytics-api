from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/api/home')
def homepage():
    return render_template('index.html')

@app.route('/api/yna')
def easter_egg():
    return render_template('yna.html')

if __name__ == '__main__':
    pass