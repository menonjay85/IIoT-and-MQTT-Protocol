import paho.mqtt.client as mqtt

# MQTT Setup  
mqttBroker = 'test.mosquitto.org'
port = 1883
topic = 'jay/machine1/temp'
topic2 = 'jay/machine1/status'
topic3 = 'jay/machine1/pressure'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected with result code {rc}")
        client.subscribe(topic)
        client.subscribe(topic2)
        client.subscribe(topic3)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    if msg.topic == topic:
        print(f"Temperature: {msg.payload.decode()} C")
    if msg.topic == topic2:
        print(f"Status: {msg.payload.decode()} ")
    if msg.topic == topic3:
        print(f"Pressure: {msg.payload.decode()} bar")

client = mqtt.Client(client_id="unique_client_id")

# Set callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(mqttBroker, port, keepalive=60)

# Start the network loop
client.loop_forever()
