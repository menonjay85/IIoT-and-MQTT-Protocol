import numpy as np
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt
import time

def simulate_mixing_speed(total_time, time_step, time):
    # Time settings
    total_time = 20  # total simulation time in seconds
    time_step = 0.01  # time step in seconds
    time = np.arange(0, total_time, time_step)

    # Spindle speed settings
    ramp_time = 10  # time to ramp up to maximum speed in seconds
    max_speed = 3000  # maximum spindle speed in rpm
    steady_speed = 2700  # average steady spindle speed in rpm
    steady_variation = 100  # variation in steady spindle speed in rpm

    # Initialize spindle speed array
    mixing_speed = np.zeros_like(time)

    # Ramp up phase
    ramp_up_indices = time <= ramp_time
    mixing_speed[ramp_up_indices] = (max_speed / ramp_time) * time[ramp_up_indices]

    # Steady phase
    steady_indices = time > ramp_time
    steady_time = time[steady_indices] - ramp_time
    mixing_speed[steady_indices] = steady_speed + steady_variation * np.sin(2 * np.pi * steady_time)

    return mixing_speed

# MQTT setup
broker = 'broker.hivemq.com'
port = 1883
topic_machine_state = 'starly/reactor/1200_state/status'
topic_temp = 'starly/reactor/1200_state/temperature'
topic_speed = 'starly/reactor/1200_state/speed'
topic_pH = 'starly/reactor/1200_state/pH'

client = mqtt.Client()

# Connect to the MQTT broker
client.connect(broker, port, 60)

# Time parameters
total_time_units = 50
time_steps = 1000
time_data = np.linspace(0, total_time_units, time_steps)  # Simulating for 10 time units

# Temperature parameters
base_temp = 37  # Base temperature in Celsius
temp_variation = 5  # Base temperature variation
spike_temp = 70  # Spike temperature in Celsius
decay_rate = 0.1  # Rate at which temperature decays back to 37C

# Simulate temperature with spikes and exponential decay
temperature = base_temp + temp_variation * np.sin(2 * np.pi * time_data)
for i in range(time_steps):
    if 2 < time_data[i] < 3 or 5 < time_data[i] < 6:
        temperature[i] = spike_temp
    elif i > 0 and (3 <= time_data[i] < 5 or 6 <= time_data[i]):
        temperature[i] = temperature[i-1] + (base_temp - temperature[i-1]) * decay_rate

# pH Value variation
min_pH = 6.7  # Minimum pH
max_pH = 8.0  # Maximum pH

# Simulate mixing speed in a simple way
np.random.seed(0)  # For reproducibility
mixing_pH = np.random.uniform(min_pH, max_pH, time_steps)

# Simulate through a slow ramp up, holding steady and varying around a mean.
mixing_speed = simulate_mixing_speed(total_time_units, time_steps, time_data)

# Publish data to MQTT broker
for t, temp, speed, pH in zip(time_data, temperature, mixing_speed, mixing_pH):
    temp_message = f'{temp:.2f}'
    speed_message = f'{speed:.2f}'
    pH_message = f'{pH:.2f}'
    machine_state_message = "ON"
    client.publish(topic_temp, temp_message)
    client.publish(topic_speed, speed_message)
    client.publish(topic_pH, pH_message)
    client.publish(topic_machine_state, machine_state_message)
    print(temp, speed, pH, machine_state_message)
    time.sleep(3)  # Simulate real-time data publishing
else:
    machine_state_message="OFF"
    client.publish(topic_machine_state, machine_state_message)
