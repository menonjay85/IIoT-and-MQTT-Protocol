import paho.mqtt.client as mqtt

# MQTT setup
broker = 'broker.hivemq.com'
port = 1883
topic_machine_state = 'starly/reactor/1200_state/status'
topic_temp = 'starly/reactor/1200_state/temperature'
topic_speed = 'starly/reactor/1200_state/speed'
topic_pH = 'starly/reactor/1200_state/ph'

# Callback when the client receives a connection response from the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to the temperature and mixing speed topics
    client.subscribe(topic_temp)
    client.subscribe(topic_speed)
    client.subscribe(topic_pH)
    client.subscribe(topic_machine_state)

# Callback when a PUBLISH message is received from the broker
def on_message(client, userdata, msg):
    if msg.topic == topic_temp:
        print(f"Temperature: {msg.payload.decode()} °C")
    if msg.topic == topic_machine_state:
        print(f"Status(ON/OFF): {msg.payload.decode()}")
    if msg.topic == topic_pH:
        print(f"pH: {msg.payload.decode()}")
    if msg.topic == topic_speed:
        print(f"Mixing Speed: {msg.payload.decode()} RPM")

client = mqtt.Client()

# Assign the on_connect and on_message callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker, port, 60)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting
client.loop_forever()
