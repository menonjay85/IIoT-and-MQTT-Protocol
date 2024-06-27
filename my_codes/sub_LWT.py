import paho.mqtt.client as mqtt
import random
import time

# MQTT Settings
port = 1883
#broker = "broker.hivemq.com"
broker = "test.mosquitto.org"
topic = 'jay/machine1/sensor1/temperature'
will_topic = 'jay/machine1/sensor1/will' # Will Topic Address

# Define the MQTT client
client = mqtt.Client()

def on_connect(client, userData, flags, rc):
    if rc == 0:
        print("Subsriber is connected to the Mosquitto Broker")

        client.subscribe(topic)
        client.subscribe(will_topic)

def on_message(client, userdata, msg):
    if msg.topic == topic:
        print("Received message: ", msg.payload.decode())
    if msg.topic == will_topic:
        print("Received message from Broker!: ", msg.payload.decode())

def on_disconnect(client, userdata, rc):
    if rc == 0:
        print("Clean Disconnection")
    if rc != 0:
        print("Unexpected Disconnection")
    

# Assign the call backs
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Connect to the Broker
client.connect(broker, port, keepalive=60)

# Start the loop
client.loop_start()

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Disconnecting from the Broker...")

client.disconnect()
client.loop_stop()