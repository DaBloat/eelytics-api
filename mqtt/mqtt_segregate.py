import time
import redis
import paho.mqtt.client as mqtt
import json

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def on_message(client, userdata, msg):
    if msg.topic == "eelytics/tank/status":
        # Save the live ESP32 data straight to Redis for your GET api
        r.set('latest_tank_stat', msg.payload.decode())
        print(f"[MQTT] Received Live Tank Data: {msg.payload.decode()}")
        
client = mqtt.Client()
client.on_message = on_message
client.connect("127.0.0.1", 1883, 60)
client.subscribe('eelytics/tank/status')
client.loop_start()
TOPIC = "eelytics/servos"

last_state = "NONE"

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
                client.publish(TOPIC, "45,0")
                print("[MQTT] Sent: 45,0 (RESET)")
            
            elif current_group == "TABLE":
                client.publish(TOPIC, "45,0")
                print("[MQTT] Sent: 45,0 (TABLE)")
                
            elif current_group == "KUROKO":
                client.publish(TOPIC, "0,0")
                print("[MQTT] Sent: 0,0 (KUROKO)")

            elif current_group == "ELVER":
                client.publish(TOPIC, "45,45")
                print("[MQTT] Sent: 45,45 (ELVER)")

            last_state = current_group

    except Exception as e:
        print(f"Error in controller loop: {e}")
        
    time.sleep(0.1)