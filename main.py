from pinpong.board import Board, gcore
from pinpong.libs.dfrobot_mpu6050 import MPU6050
from unihiker import GUI, Audio, Button, Slider
import time
import math

# Initialize the Board, MPU6050 sensor, GUI, Audio, Button, and Slider
Board("unihiker").begin()
i2c = gcore.i2c0
mpu = MPU6050(i2c)
gui = GUI()
audio = Audio()
reset_button = Button(270, 200, "Reset Center", width=150, height=40)
threshold_slider = Slider(20, 200, width=200, height=30, min_value=0.05, max_value=0.5, value=0.1)

# Variables for calibration and smooth animation
calibration_x = 0
calibration_y = 0
current_x = 160
current_y = 120

# Function to calculate the tilt angle
def calculate_tilt_angle(x, y):
    return math.degrees(math.atan2(y, x))

# Function to get the lean direction, display it, and handle feedback
def get_lean_direction(threshold):
    global calibration_x, calibration_y
    
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
    
    # Clear the screen and display the direction, angle, and feedback
    gui.clear()
    
    # Set background color based on direction
    if direction == "Centered":
        bg_color = (0, 255, 0)  # Green for centered
    else:
        bg_color = (255, 0, 0)  # Red for leaning
    gui.background(bg_color)
    
    # Display the direction, tilt angle, and threshold value
    gui.text(80, 60, "Direction:", color=(255, 255, 255), size=24)
    gui.text(100, 100, direction, color=(255, 255, 255), size=36)
    gui.text(80, 160, f"Tilt Angle: {angle:.2f}°", color=(255, 255, 255), size=24)
    gui.text(80, 220, f"Threshold: {threshold:.2f}", color=(255, 255, 255), size=24)
    
    return direction, angle, x, y

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

# Main loop
while True:
    # Check for reset calibration
    if reset_button.is_pressed():
        accel = mpu.acceleration()
        calibration_x = accel[0]
        calibration_y = accel[1]
        gui.text(60, 180, "Calibration reset!", color=(255, 255, 0), size=24)
        time.sleep(1)
    
    # Get current threshold value from the slider
    threshold = threshold_slider.get_value()
    
    # Get lean direction, angle, and target position
    direction, angle, target_x, target_y = get_lean_direction(threshold)
    
    # Animate the arrow smoothly towards the target position
    animate_arrow(160 + int(target_x * 100), 120 - int(target_y * 100))
    
    print(f"Direction: {direction}, Tilt Angle: {angle:.2f}°, Threshold: {threshold:.2f}")
    time.sleep(0.1)
