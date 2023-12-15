import serial
import datetime

# Set up serial connection (adjust COM port as needed)
ser = serial.Serial('COM3', 9600, timeout=1)

# Open a file to write
with open("serial_data.csv", "w") as file:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            timestamp = datetime.datetime.now().microsecond
            file.write(f"{timestamp},{line}\n")
            print(f"{timestamp},{line}")  # Optional: to see the output in the console
