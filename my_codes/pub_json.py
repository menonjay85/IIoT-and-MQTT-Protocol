import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
from datetime import datetime
import json


# MQTT Settings
port = 1883
#broker = "broker.hivemq.com"
broker = "test.mosquitto.org"
topic = 'jay/machine1/sensors'
will_topic = 'jay/machine1/will' # Will Topic Address
will_msg = "One or more sensors has disconnected unexpectedly" # LWT Message Brodcasted

client = mqtt.Client()
client.connect(broker, port, keepalive=60)
client.will_set(will_topic, will_msg, qos=1, retain=False)

# Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connection has been established")
    else:
        print("Connection not established")

def on_disconnect(client, userdata, rc):
    if rc == 0:
        print("Clean Disconnection")
    if rc != 0:
        print("Unexpected Disconnection")

def on_publish(client, userdata, rc):
    print("Message published")

def on_log(client, userdata, level, buffer):
    print("Log: ", buffer)


# Assign the call backs
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.on_log = on_log

data = {}

client.loop_start()
try:
    while True:
        temp = uniform(20,30)
        Terror = round(uniform(-3,3),3)

        pressure = uniform(1, 10)
        Perror = round(uniform(-1,1),2)

        now = datetime.now().date()
        timestamp = datetime.now()

        #configue the JSON object
        data["date"] = str(now)
        data["timestamp"] = str(timestamp)
        data["Temperature"] = (temp, Terror)
        data["Pressure"] = (pressure, Perror)
        
        jsondata = json.dumps(data)
        client.publish(topic, jsondata, qos=1)
        time.sleep(3)

except KeyboardInterrupt:
    print("Disconnected the server")

client.loop_stop()