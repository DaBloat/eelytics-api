from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mqtt import Mqtt
import json
import os # Useful for environment variables
from sqlalchemy import text # Import the text function

# --- 1. CORE APPLICATION SETUP ---
app = Flask(__name__)

# --- 2. CONFIGURATION ---
# Database URI - Ensure this user/pass/db exists in PostgreSQL
# NOTE: Using environment variables for the password is much safer in production!
DB_PASSWORD = 'your_secure_db_password' # Replace with actual password
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://eelytics_admin:traceydee15@localhost/eelytics_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# MQTT Configuration
app.config['MQTT_BROKER_URL'] = '127.0.0.1' 
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 5  
app.config['MQTT_TLS_ENABLED'] = False
# Optionally add credentials here if you configure Mosquitto authentication
app.config['MQTT_USERNAME'] = '' 
app.config['MQTT_PASSWORD'] = '' 

# --- 3. INITIALIZE EXTENSIONS ---
db = SQLAlchemy(app)
mqtt = Mqtt(app)

# --- 4. DATABASE MODELS ---
class WaterLevel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tank_id = db.Column(db.Integer, nullable=False)
    level_cm = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<WaterLevel Tank {self.tank_id} Level {self.level_cm}>'


# --- 5. HELPER FUNCTIONS (for publishing commands) ---
def send_gate_command(tank_id, command):
    """Publishes a command message to a specific ESP32 Gate."""
    topic = f'command/gate/{tank_id}/action'
    payload = json.dumps({'action': command})
    # mqtt.publish requires an application context when run outside a request/event handler
    with app.app_context():
        mqtt.publish(topic, payload)
        # Print to Gunicorn logs for visibility
        print(f"[CMD] Published: {payload} to {topic}")

# --- 6. MQTT HANDLERS (Decorators now work as 'mqtt' is defined) ---

# 6.1 Successful Connection
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT] Broker connection successful!")
        # Subscribe to all sensor topics on connection
        mqtt.subscribe('sensor/tank/+/water_level')  
        mqtt.subscribe('sensor/gate/+/status')
    else:
        print(f'[MQTT] Connection failed with code {rc}')

# 6.2 Message Reception and Database Logging
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    # This runs in a separate thread, so app context is mandatory for DB
    with app.app_context():
        try:
            topic_parts = message.topic.split('/')
            data = json.loads(message.payload.decode())
            
            # Check if this is a water level message
            if topic_parts[1] == 'tank' and topic_parts[3] == 'water_level':
                tank_id = topic_parts[2]
                
                # 3. Create and commit to the database
                level = WaterLevel(
                    tank_id=int(tank_id), 
                    level_cm=data['level'],
                )
                db.session.add(level)
                db.session.commit()
                print(f"[DB LOG] Tank {tank_id}: Logged Level {data['level']} cm")
                
            # Add other data processing logic here (e.g., eel segmentation data from laptop)

        except Exception as e:
            # IMPORTANT: Rollback the session if there's an error to prevent DB lock
            db.session.rollback() 
            print(f"[ERROR] MQTT Message processing error: {e}")
            print(f"Failed Payload: {message.payload.decode()}")

# --- 7. HTTP ROUTES (Web API Endpoints) ---
@app.route('/')
def home():
    db_status = "error"
    db_error = None
    
    with app.app_context():
        try:
            # CORRECTED: Use a simple select(1) for a lightweight health check
            db.session.execute(db.select(1))
            db_status = "ok"
        except Exception as e:
            db_status = "error"
            db_error = str(e)
            
    response = {
        "status": "Eelytics API is Live", 
        "mqtt_status": mqtt.connected,
        "db_status": db_status
    }
    
    if db_error:
        response["db_error_message"] = db_error

    return jsonify(response)

# Example API endpoint to retrieve all water level data
@app.route('/api/levels', methods=['GET'])
def get_levels():
    # Use app_context for any query operation
    with app.app_context():
        levels = db.session.execute(db.select(WaterLevel).order_by(WaterLevel.timestamp.desc())).scalars().all()
        
        # Convert SQLAlchemy objects to list of dictionaries for JSON response
        levels_list = [
            {
                'id': level.id,
                'tank_id': level.tank_id,
                'level_cm': level.level_cm,
                'timestamp': level.timestamp.isoformat()
            } for level in levels
        ]
        return jsonify(levels_list)
        
# Example API endpoint for the Mobile App to send a command
@app.route('/api/command/gate/<int:tank_id>', methods=['POST'])
def api_command_gate(tank_id):
    # This is a good place to add authentication/validation for the mobile app
    # For now, we assume the command is in the request JSON body: {"action": "open" | "close"}
    try:
        data = request.get_json()
        command = data.get('action')
        
        if command in ['open', 'close']:
            send_gate_command(tank_id, command)
            return jsonify({"status": "Command sent", "tank_id": tank_id, "action": command}), 200
        else:
            return jsonify({"error": "Invalid command"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- 8. DEVELOPMENT RUN (Ignored by Gunicorn) ---
if __name__ == '__main__':
    # When running directly (python wsgi.py), create tables first
    with app.app_context():
        db.create_all()
        print("Database tables ensured.")
        
    # Gunicorn ignores this line, but for direct testing:
    # app.run(host='0.0.0.0', port=5000, debug=True)
    pass # Keep this simple since Gunicorn handles the service

