from machine import I2C
from imu import MPU6050
import time

# Initialize I2C communication and MPU6050 sensor
i2c = I2C(0, scl=22, sda=21)
mpu = MPU6050(i2c)

def get_lean_direction():
    # Read accelerometer values
    accel = mpu.accel
    x = accel.x
    y = accel.y
    
    # Determine leaning direction based on X and Y axes
    if x > 0.1:
        return "Leaning Right"
    elif x < -0.1:
        return "Leaning Left"
    elif y > 0.1:
        return "Leaning Forward"
    elif y < -0.1:
        return "Leaning Backward"
    else:
        return "Centered"

# Main loop
while True:
    direction = get_lean_direction()
    print("Direction:", direction)
    time.sleep(0.5)
