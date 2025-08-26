import RPi.GPIO as GPIO
import time
from minisom import MiniSom
import numpy as np

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor Driver 1 (left motors) Pin Assignments
ena1, enb1 = 18, 19
in1_1, in2_1, in3_1, in4_1 = 22, 27, 23, 24
# Motor Driver 2 (right motors) Pin Assignments
ena2, enb2 = 12, 16
in1_2, in2_2, in3_2, in4_2 = 6, 5, 13, 26
# Ultrasonic Sensor Pins
trigger_left, echo_left = 17, 20
trigger_right, echo_right = 21, 25
trigger_left_diag, echo_left_diag = 7, 8
trigger_right_diag, echo_right_diag = 9, 10

# Movement Matrix for storing actions and time
movement_matrix = []

# Motor Setup
def motor_setup():
    motor_pins = [ena1, enb1, in1_1, in2_1, in3_1, in4_1, ena2, enb2,
                  in1_2, in2_2, in3_2, in4_2]
    for pin in motor_pins:
        GPIO.setup(pin, GPIO.OUT)

# Motor Control Functions
def move_forward():
    GPIO.output(in1_1, GPIO.HIGH)
    GPIO.output(in2_1, GPIO.LOW)
    GPIO.output(in3_1, GPIO.HIGH)
    GPIO.output(in4_1, GPIO.LOW)
    GPIO.output(in1_2, GPIO.HIGH)
    GPIO.output(in2_2, GPIO.LOW)
    GPIO.output(in3_2, GPIO.HIGH)
    GPIO.output(in4_2, GPIO.LOW)
    record_movement('move_forward')

def turn_left():
    GPIO.output(in1_1, GPIO.LOW)
    GPIO.output(in2_1, GPIO.HIGH)
    GPIO.output(in3_1, GPIO.HIGH)
    GPIO.output(in4_1, GPIO.LOW)
    GPIO.output(in1_2, GPIO.HIGH)
    GPIO.output(in2_2, GPIO.LOW)
    GPIO.output(in3_2, GPIO.LOW)
    GPIO.output(in4_2, GPIO.HIGH)
    record_movement('turn_left')

def turn_right():
    GPIO.output(in1_1, GPIO.HIGH)
    GPIO.output(in2_1, GPIO.LOW)
    GPIO.output(in3_1, GPIO.LOW)
    GPIO.output(in4_1, GPIO.HIGH)
    GPIO.output(in1_2, GPIO.LOW)
    GPIO.output(in2_2, GPIO.HIGH)
    GPIO.output(in3_2, GPIO.HIGH)
    GPIO.output(in4_2, GPIO.LOW)
    record_movement('turn_right')

def stop():
    GPIO.output(in1_1, GPIO.LOW)
    GPIO.output(in2_1, GPIO.LOW)
    GPIO.output(in3_1, GPIO.LOW)
    GPIO.output(in4_1, GPIO.LOW)
    GPIO.output(in1_2, GPIO.LOW)
    GPIO.output(in2_2, GPIO.LOW)
    GPIO.output(in3_2, GPIO.LOW)
    GPIO.output(in4_2, GPIO.LOW)
    record_movement('stop')

# Record the movement and timestamp in the matrix
def record_movement(action):
    current_time = time.time()
    movement_matrix.append([action, current_time])

# Ultrasonic Sensor Functions
def setup_ultrasonic(trigger, echo):
    GPIO.setup(trigger, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)

def get_distance(trigger, echo):
    GPIO.output(trigger, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigger, GPIO.LOW)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(echo) == 0:
        start_time = time.time()

    while GPIO.input(echo) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2
    return distance

# MiniSOM Initialization
som = MiniSom(x=3, y=3, input_len=4, sigma=1.0, learning_rate=0.5)
training_data = [] # Placeholder for collected ultrasonic data

# Training the SOM (replace with actual data collection and training)
training_data = [
    [30, 30, 50, 50],  # Move forward
    [15, 30, 50, 50],  # Turn right
    [30, 15, 50, 50],  # Turn left
    [10, 10, 20, 20],  # Obstacle ahead
]
som.random_weights_init(training_data)
som.train_random(training_data, 100) # 100 iterations

# Navigation Logic
def navigate():
    dist_left = get_distance(trigger_left, echo_left)
    dist_right = get_distance(trigger_right, echo_right)
    dist_left_diag = get_distance(trigger_left_diag, echo_left_diag)
    dist_right_diag = get_distance(trigger_right_diag, echo_right_diag)

    input_data = np.array([dist_left, dist_right, dist_left_diag,
                           dist_right_diag])
    winner = som.winner(input_data)

    # Control logic based on SOM output
    if winner == (0, 0):
        move_forward()
    elif winner == (0, 1):
        turn_right()
    elif winner == (1, 0):
        turn_left()
    else:
        stop()

# Main Loop
if __name__ == "__main__":
    try:
        motor_setup()
        setup_ultrasonic(trigger_left, echo_left)
        setup_ultrasonic(trigger_right, echo_right)
        setup_ultrasonic(trigger_left_diag, echo_left_diag)
        setup_ultrasonic(trigger_right_diag, echo_right_diag)
        
        while True:
            navigate()
            time.sleep(0.1) # Delay between cycles
            
    except KeyboardInterrupt:
        stop()
        GPIO.cleanup()
        print("Program terminated.")
        print("Movement Log:", movement_matrix)