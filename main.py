from pinpong.board import Board, gcore
from pinpong.libs.dfrobot_mpu6050 import MPU6050
from unihiker import GUI, Audio
import time
import math

# Initialize the Board, MPU6050 sensor, GUI, and Audio
Board("unihiker").begin()
i2c = gcore.i2c0
mpu = MPU6050(i2c)
gui = GUI()
audio = Audio()

# Function to calculate the tilt angle
def calculate_tilt_angle(x, y):
    return math.degrees(math.atan2(y, x))

# Function to get the lean direction, display it, and handle feedback
def get_lean_direction():
    # Read accelerometer values
    accel = mpu.acceleration()
    x = accel[0]
    y = accel[1]
    
    # Calculate the tilt angle
    angle = calculate_tilt_angle(x, y)
    
    # Determine leaning direction
    if x > 0.1:
        direction = "Right"
    elif x < -0.1:
        direction = "Left"
    elif y > 0.1:
        direction = "Forward"
    elif y < -0.1:
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
    
    # Display the direction and tilt angle
    gui.text(80, 60, "Direction:", color=(255, 255, 255), size=24)
    gui.text(100, 100, direction, color=(255, 255, 255), size=36)
    gui.text(80, 160, f"Tilt Angle: {angle:.2f}°", color=(255, 255, 255), size=24)
    
    # Draw an arrow to indicate the direction
    center_x, center_y = 160, 120
    if direction == "Right":
        gui.line(center_x, center_y, center_x + 50, center_y, color=(255, 255, 255), size=5)
    elif direction == "Left":
        gui.line(center_x, center_y, center_x - 50, center_y, color=(255, 255, 255), size=5)
    elif direction == "Forward":
        gui.line(center_x, center_y, center_x, center_y - 50, color=(255, 255, 255), size=5)
    elif direction == "Backward":
        gui.line(center_x, center_y, center_x, center_y + 50, color=(255, 255, 255), size=5)
    else:
        gui.circle(center_x, center_y, 20, color=(255, 255, 255), fill=True)
    
    return direction, angle

# Main loop
while True:
    direction, angle = get_lean_direction()
    print(f"Direction: {direction}, Tilt Angle: {angle:.2f}°")
    time.sleep(0.5)
