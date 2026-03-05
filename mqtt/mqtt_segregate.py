import time
import redis
import paho.mqtt.client as mqtt
import json

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def on_message(client, userdata, msg):
    if msg.topic == "eelytics/tank/status":
        r.set('latest_tank_stat', msg.payload.decode())
        print(f"[MQTT] Received Live Tank Data: {msg.payload.decode()}")
        
client = mqtt.Client()
client.on_message = on_message
client.connect("127.0.0.1", 1883, 60)
client.subscribe('eelytics/tank/status')
client.loop_start()
GATE_TOPIC = "eelytics/servos"
TANK_TOPIC = "eelytics/tank/control"

last_state = "NONE"
last_state_opt = None

print("Starting Eel Controller Service...")

while True:
    try:
        raw_data = r.get('latest_eel')
        
        if raw_data:
            data = json.loads(raw_data)
            current_group = data.get("group", "NONE")
        else:
            current_group = "NONE"

        if current_group != last_state:
            if current_group == "NONE":
                client.publish(GATE_TOPIC, "45,0")
                print("[MQTT] Sent: 45,0 (RESET)")
            
            elif current_group == "TABLE":
                client.publish(GATE_TOPIC, "45,0")
                print("[MQTT] Sent: 45,0 (TABLE)")
                
            elif current_group == "KUROKO":
                client.publish(GATE_TOPIC, "0,0")
                print("[MQTT] Sent: 0,0 (KUROKO)")

            elif current_group == "ELVER":
                client.publish(GATE_TOPIC, "45,45")
                print("[MQTT] Sent: 45,45 (ELVER)")

            last_state = current_group
            
        raw_data_opt = r.get('latest_tank_opt')
        if raw_data_opt and raw_data_opt != last_state_opt:
            client.publish(TANK_TOPIC, raw_data_opt)
            print(f"[MQTT] Set {raw_data_opt} as new Settings")
            
            last_state_opt = raw_data_opt
            
    except Exception as e:
        print(f"Error in controller loop: {e}")
        
    time.sleep(0.1)