import paho.mqtt.client as mqtt
import random
import time

# MQTT Settings
port = 1883
#broker = "broker.hivemq.com"
broker = "test.mosquitto.org"
topic = 'jay/machine1/sensors'
will_topic = 'jay/machine1/will' # Will Topic Address

client = mqtt.Client()
client.connect(broker, port, keepalive=60)

def on_connect(client, userData, flags, rc):
    if rc == 0:
        print("Subsriber is connected to the Mosquitto Broker")

        client.subscribe(topic)
        client.subscribe(will_topic)

def on_message(client, userdata, msg):
    if msg.topic == topic:
        print("Received message: ", msg.payload.decode())

def on_disconnect(client, userdata, rc):
    if rc == 0:
        print("Clean Disconnection")
    if rc != 0:
        print("Unexpected Disconnection")

def on_log(client, userdata, level, buffer):
    print("Log: ", buffer)

# Assign the call backs
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_log = on_log


# Start the loop
client.loop_start()

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Disconnecting from the Broker...")

client.disconnect()
client.loop_stop()