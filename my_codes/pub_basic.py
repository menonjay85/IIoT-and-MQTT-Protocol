import paho.mqtt.client as mqtt
from random import uniform
import time

# MQTT Setup  
port = 1883
mqttBroker = 'test.mosquitto.org'
topic = 'jay/machine1/temp'

topic2 = 'jay/machine1/status'
topic3 = 'jay/machine1/pressure'

counter = 0

client = mqtt.Client()

# Send connection request
client.connect(mqttBroker, port, keepalive=60)

# Simulate a sensor
while True:
    # randomly simulated value
    randTemp = uniform(20.0, 25.0)
    status = 'ON'
    randPress = uniform(1.0, 10.0)
    
    # Below publishes to the specific broker
    client.publish(topic, randTemp, qos=0)
    client.publish(topic2, status, qos=0)
    client.publish(topic3, randPress, qos=0)
    print(f"Data {status}: {randTemp} C : {randPress} bar")

    # Switch off the machine after 50 values are published
    counter+=1
    if counter % 50 == 0:
        status = 'OFF'
        randTemp = 0
        randPress = 0
        client.publish(topic, randTemp, qos=0)
        client.publish(topic2, status, qos=0)
        client.publish(topic3, randPress, qos=0)
        time.sleep(10)
    else:
        time.sleep(2)


