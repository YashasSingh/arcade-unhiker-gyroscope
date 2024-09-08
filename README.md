
# Unihiker Tilt Monitoring System
![image](https://github.com/user-attachments/assets/5e1f4e08-af0d-4336-8bcb-79079c779242)


This project is a tilt monitoring system for the Unihiker device, utilizing its built-in MPU6050 gyroscope and accelerometer. The system determines which direction the device is leaning relative to a target center and provides visual, audio, and logged feedback. The project leverages the `pinpong` and `unihiker` libraries to interact with the hardware components.

## Features

- **Real-Time Tilt Detection**: Continuously monitors the tilt of the Unihiker and displays the direction (left, right, forward, backward, or centered).
- **Tilt Angle Calculation**: Calculates and displays the tilt angle in degrees.
- **Audio Feedback**: Plays a sound alert when the tilt angle exceeds a predefined threshold.
- **Data Logging**: Logs tilt direction, angle, and timestamp to a CSV file for later analysis.
- **Real-Time Graph**: Displays a real-time graph of the tilt angle.
- **User Interface**: Features an interactive UI with a reset button for calibration, a slider to adjust the sensitivity threshold, and a menu system for navigating different options.
- **Battery Monitoring**: Displays the current battery level of the Unihiker.
- **Error Handling**: Includes error handling mechanisms to manage unexpected sensor failures or file I/O errors.

## Getting Started

### Prerequisites

- Unihiker device
- Python environment with `pinpong` and `unihiker` libraries installed

### Installation

1. Clone this repository to your Unihiker:
    ```sh
    git clone <repository-url>
    ```
2. Navigate to the project directory:
    ```sh
    cd unihiker-tilt-monitor
    ```
3. Ensure the `pinpong` and `unihiker` libraries are installed:
    ```sh
    pip install pinpong unhiker
    ```

### Usage

1. **Run the Program**:
    - Connect the Unihiker to your computer.
    - Execute the Python script:
    ```sh
    python tilt_monitor.py
    ```
2. **Calibrate the Device**:
    - Place the Unihiker on a flat surface and press the "Reset Center" button to calibrate the gyroscope.
3. **Adjust Sensitivity**:
    - Use the slider to adjust the threshold for detecting tilt direction.

### Data Logging

Tilt data is logged to a file named `tilt_log.csv` located in the same directory as the script. Each entry includes:

- Timestamp
- Direction (Left, Right, Forward, Backward, Centered)
- Tilt Angle (in degrees)

### Real-Time Graph

A real-time graph displays the tilt angle, updating as new data is received. The graph shows up to 100 data points and provides a visual representation of the device's movement.

### Error Handling

The program includes basic error handling for sensor reading and file I/O operations. If an error occurs, it will be logged to the console, and the program will continue running.

### Battery Monitoring

The current battery level of the Unihiker is displayed on the screen. A battery icon or bar graph represents the remaining power, helping to manage the device's power consumption.

### Menu System

A simple menu system allows users to navigate between different features (e.g., viewing logs, adjusting settings, etc.). This is a placeholder for future expansions.

## Customization

### Adding New Features

Feel free to expand this project with additional features, such as:

- **Advanced Calibration**: Implement a more guided calibration process.
- **Power Management**: Introduce sleep modes or low-power states for better battery life.
- **External Communication**: Add features for exporting data via USB, Bluetooth, or Wi-Fi.

### Code Structure

- `tilt_monitor.py`: Main script for the tilt monitoring system.
- `tilt_log.csv`: Log file where tilt data is recorded.

### Troubleshooting

- **No Data Logging**: Ensure that the Unihiker has the necessary permissions to write files in the project directory.
- **Sensor Issues**: Check connections and ensure the MPU6050 sensor is functioning correctly.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **pinpong Library**: For providing easy access to the MPU6050 sensor and other hardware components.
- **unihiker Library**: For enabling smooth interaction with the Unihiker's UI and audio features.

## Contact

For further questions, enhancements, or contributions, please open an issue on the repository or contact the project maintainer.

