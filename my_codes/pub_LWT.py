import paho.mqtt.client as mqtt
import random
import time

# MQTT Settings
port = 1883
#broker = "broker.hivemq.com"
broker = "test.mosquitto.org"
topic = 'jay/machine1/sensor1/temperature'

will_topic = 'jay/machine1/sensor1/will' # Will Topic Address
will_msg = "Sensor 1 has disconnected unexpectedly" # LWT Message Brodcasted

# Define the MQTT client
client = mqtt.Client()
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

# Assign the call backs
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

# Connect to the broker
client.connect(broker, port, keepalive=60)

client.loop_start()

# Simulate publishing sensor data
try:
    for i in range (1000):
        temperature = round(random.uniform(20, 30), 2)

        # Publish the value and where
        client.publish(topic, temperature)

        time.sleep(2)

    # Simulate a disconnection of the publisher
    client._sock_close() # Force the port socket to be closed

except KeyboardInterrupt:
    print("Disconnecting the Server")

# Disconnect from the broker
client.disconnect()

# Stop the loop
client.loop_stop()