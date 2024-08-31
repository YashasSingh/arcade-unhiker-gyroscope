from pinpong.board import Board, gcore
from pinpong.libs.dfrobot_mpu6050 import MPU6050
from unihiker import GUI, Audio, Button, Slider, Battery
import time
import math
import csv
import os

# Initialize the Board, MPU6050 sensor, GUI, Audio, Button, Slider, and Battery
Board("unihiker").begin()
i2c = gcore.i2c0
mpu = MPU6050(i2c)
gui = GUI()
audio = Audio()
reset_button = Button(270, 200, "Reset Center", width=150, height=40)
threshold_slider = Slider(20, 200, width=200, height=30, min_value=0.05, max_value=0.5, value=0.1)
battery = Battery()

# Variables for calibration and smooth animation
calibration_x = 0
calibration_y = 0
current_x = 160
current_y = 120

# Data logging setup
log_file = "tilt_log.csv"
if not os.path.exists(log_file):
    with open(log_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Direction", "Tilt Angle"])

# Real-time graph data
graph_data = []
max_graph_points = 100  # Maximum number of points to display

# Function to calculate the tilt angle
def calculate_tilt_angle(x, y):
    return math.degrees(math.atan2(y, x))

# Function to log data to CSV
def log_data(direction, angle):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        with open(log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, direction, f"{angle:.2f}"])
    except Exception as e:
        print(f"Error logging data: {e}")

# Function to get the lean direction, display it, and handle feedback
def get_lean_direction(threshold):
    global calibration_x, calibration_y
    
    try:
        # Read accelerometer values
        accel = mpu.acceleration()
        x = accel[0] - calibration_x
        y = accel[1] - calibration_y
        
        # Calculate the tilt angle
        angle = calculate_tilt_angle(x, y)
        
        # Determine leaning direction
        if x > threshold:
            direction = "Right"
        elif x < -threshold:
            direction = "Left"
        elif y > threshold:
            direction = "Forward"
        elif y < -threshold:
            direction = "Backward"
        else:
            direction = "Centered"
        
        # Play a sound if the tilt angle exceeds a threshold (e.g., 15 degrees)
        if abs(angle) > 15:
            audio.play_tone(1000, 200)  # 1kHz tone for 200ms
        
        # Log the data
        log_data(direction, angle)
        
        # Add data to graph
        graph_data.append(angle)
        if len(graph_data) > max_graph_points:
            graph_data.pop(0)
        
        return direction, angle, x, y
    except Exception as e:
        print(f"Error reading sensor data: {e}")
        return "Error", 0.0, 0, 0

# Function to animate arrow movement
def animate_arrow(target_x, target_y):
    global current_x, current_y
    
    step = 5
    if abs(current_x - target_x) > step:
        current_x += step if current_x < target_x else -step
    if abs(current_y - target_y) > step:
        current_y += step if current_y < target_y else -step
    
    # Draw arrow at the current position
    gui.line(160, 120, current_x, current_y, color=(255, 255, 255), size=5)

# Function to display real-time graph
def display_graph():
    gui.rect(20, 250, 300, 100, color=(50, 50, 50), fill=True)
    if len(graph_data) < 2:
        return
    max_angle = max(graph_data)
    min_angle = min(graph_data)
    range_angle = max_angle - min_angle if max_angle != min_angle else 1
    for i in range(len(graph_data)-1):
        x1 = 20 + (i / max_graph_points) * 300
        y1 = 250 + 100 - ((graph_data[i] - min_angle) / range_angle) * 100
        x2 = 20 + ((i+1) / max_graph_points) * 300
        y2 = 250 + 100 - ((graph_data[i+1] - min_angle) / range_angle) * 100
        gui.line(x1, y1, x2, y2, color=(0, 255, 255), size=2)
    gui.text(320, 250, "Real-Time Tilt Angle", color=(255, 255, 255), size=16)

# Function to handle calibration reset
def handle_calibration():
    global calibration_x, calibration_y
    accel = mpu.acceleration()
    calibration_x = accel[0]
    calibration_y = accel[1]
    gui.text(60, 180, "Calibration reset!", color=(255, 255, 0), size=24)
    time.sleep(1)

# Function to display battery level
def display_battery():
    batt_level = battery.get_level()
    gui.text(280, 10, f"Battery: {batt_level}%", color=(255, 255, 255), size=16)
    # Optionally, add a battery icon or bar
    gui.rect(280, 30, batt_level * 2, 10, color=(0, 255, 0), fill=True)

# Function to display menu
def display_menu():
    gui.clear()
    gui.text(150, 50, "Unihiker Tilt Monitor", color=(255, 255, 255), size=24)
    gui.text(100, 100, "1. View Logs", color=(255, 255, 255), size=20)
    gui.text(100, 140, "2. Settings", color=(255, 255, 255), size=20)
    gui.text(100, 180, "3. Exit", color=(255, 255, 255), size=20)
    gui.update()

# Main loop
def main():
    while True:
        # Check for reset calibration
        if reset_button.is_pressed():
            handle_calibration()
        
        # Get current threshold value from the slider
        threshold = threshold_slider.get_value()
        
        # Get lean direction, angle, and target position
        direction, angle, target_x, target_y = get_lean_direction(threshold)
        
        # Animate the arrow smoothly towards the target position
        target_screen_x = 160 + int(target_x * 100)
        target_screen_y = 120 - int(target_y * 100)
        animate_arrow(target_screen_x, target_screen_y)
        
        # Clear the main display area
        gui.rect(0, 0, 320, 240, color=(0, 0, 0), fill=True)
        
        # Set background color based on direction
        if direction == "Centered":
            bg_color = (0, 255, 0)  # Green for centered
        elif direction == "Error":
            bg_color = (128, 0, 128)  # Purple for error
        else:
            bg_color = (255, 0, 0)  # Red for leaning
        gui.background(bg_color)
        
        # Display the direction, tilt angle, threshold value, and battery level
        gui.text(80, 60, "Direction:", color=(255, 255, 255), size=24)
        gui.text(100, 100, direction, color=(255, 255, 255), size=36)
        gui.text(80, 160, f"Tilt Angle: {angle:.2f}°", color=(255, 255, 255), size=24)
        gui.text(80, 220, f"Threshold: {threshold:.2f}", color=(255, 255, 255), size=24)
        display_battery()
        
        # Draw an arrow to indicate the direction
        if direction != "Error":
            if direction == "Right":
                gui.line(160, 120, 160 + 50, 120, color=(255, 255, 255), size=5)
            elif direction == "Left":
                gui.line(160, 120, 160 - 50, 120, color=(255, 255, 255), size=5)
            elif direction == "Forward":
                gui.line(160, 120, 160, 120 - 50, color=(255, 255, 255), size=5)
            elif direction == "Backward":
                gui.line(160, 120, 160, 120 + 50, color=(255, 255, 255), size=5)
            else:
                gui.circle(160, 120, 20, color=(255, 255, 255), fill=True)
        
        # Display the real-time graph
        display_graph()
        
        # Print to console
        print(f"Direction: {direction}, Tilt Angle: {angle:.2f}°, Threshold: {threshold:.2f}%, Battery: {battery.get_level()}%")
        
        gui.update()
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program terminated by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
