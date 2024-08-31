from pinpong.board import Board, gcore
from pinpong.libs.dfrobot_mpu6050 import MPU6050
from unihiker import GUI
import time

# Initialize the Board, MPU6050 sensor, and GUI
Board("unihiker").begin()
i2c = gcore.i2c0
mpu = MPU6050(i2c)
gui = GUI()

# Function to get the lean direction and display it
def get_lean_direction():
    # Read accelerometer values
    accel = mpu.acceleration()
    x = accel[0]
    y = accel[1]
    
    # Determine leaning direction and display it
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
    
    # Clear the screen and display the direction
    gui.clear()
    gui.text(80, 60, "Direction:", color=(0, 0, 255), size=24)
    gui.text(100, 100, direction, color=(255, 0, 0), size=36)

    # Draw an arrow to indicate the direction
    center_x, center_y = 160, 120
    if direction == "Right":
        gui.line(center_x, center_y, center_x + 50, center_y, color=(0, 255, 0), size=5)
    elif direction == "Left":
        gui.line(center_x, center_y, center_x - 50, center_y, color=(0, 255, 0), size=5)
    elif direction == "Forward":
        gui.line(center_x, center_y, center_x, center_y - 50, color=(0, 255, 0), size=5)
    elif direction == "Backward":
        gui.line(center_x, center_y, center_x, center_y + 50, color=(0, 255, 0), size=5)
    else:
        gui.circle(center_x, center_y, 20, color=(0, 255, 0), fill=True)
    
    return direction

# Main loop
while True:
    direction = get_lean_direction()
    print("Direction:", direction)
    time.sleep(0.5)
