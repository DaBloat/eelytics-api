import time
import redis
import paho.mqtt.client as mqtt
import json

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

client = mqtt.Client()
client.connect("127.0.0.1", 1883, 60)
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