import asyncio
import matplotlib.pyplot as plt
from bleak import BleakClient, BleakScanner
from collections import defaultdict
import re
import csv
import pandas as pd


class ArduinoAccelDataCollector:
    def __init__(self, arduino_address):
        self.address = arduino_address
        self.client = BleakClient(self.address)
        self.data = defaultdict(list)

        self.Timestamps = self.data['Timestamp']
        self.AccelX = self.data['AccelX']
        self.AccelY = self.data['AccelY']
        self.AccelZ = self.data['AccelZ']
        self.GyroX = self.data['GyroX']
        self.GyroY = self.data['GyroY']
        self.GyroZ = self.data['GyroZ']

        self.SERVICE_UUID = "477fcf1c-b91c-4c23-9004-95211c661945"
        self.ACCEL_UUID = "eebf853b-a580-424c-a827-d6600f4253e1"
        self.IsDebug = False
        self.HasStarted = False

    def plot_rolling_means(self):

        accel_data = pd.DataFrame({
            'Timestamp': self.data['Timestamp'],
            'AccelX': [x[1] for x in self.data['AccelX']],
            'AccelY': [y[1] for y in self.data['AccelY']],
            'AccelZ': [z[1] for z in self.data['AccelZ']]
        })
        # Compute rolling means for smoother curves and to identify general trends
        window_size = 200
        rolling_means = accel_data.rolling(window=window_size).mean()

        # Plot the rolling means
        plt.figure(figsize=(15, 9))
        plt.plot(self.data['Timestamp'], rolling_means['AccelX'],
                 label='AccelX (Rolling Mean)')
        plt.plot(self.data['Timestamp'], rolling_means['AccelY'],
                 label='AccelY (Rolling Mean)')
        plt.plot(self.data['Timestamp'], rolling_means['AccelZ'],
                 label='AccelZ (Rolling Mean)')
        plt.title('Rolling Means of Accelerometer Readings')
        plt.legend()
        plt.grid(True)
        plt.show()

    def export_to_csv(self, filename="accel_gyro_data.csv"):
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            # Write the header
            csv_writer.writerow(
                ["Timestamp", "AccelX", "AccelY", "AccelZ", "GyroX", "GyroY", "GyroZ"])

            # Ensure all lists are of the same length
            length = min(len(self.data['Timestamp']), len(self.data['AccelX']), len(self.data['AccelY']),
                         len(self.data['AccelZ']), len(self.data['GyroX']), len(self.data['GyroY']), len(self.data['GyroZ']))

            for i in range(length):
                timestamp = self.data['Timestamp'][i]
                accelX = self.data['AccelX'][i][1]
                accelY = self.data['AccelY'][i][1]
                accelZ = self.data['AccelZ'][i][1]
                gyroX = self.data['GyroX'][i][1]
                gyroY = self.data['GyroY'][i][1]
                gyroZ = self.data['GyroZ'][i][1]

                csv_writer.writerow(
                    [timestamp, accelX, accelY, accelZ, gyroX, gyroY, gyroZ])

    async def connect(self):
        if not await self.client.connect():
            print(f"Failed to connect to {self.address}")
            return False

        services = self.client.services
        if not services:
            print("No BLE services found")
            return False

        found = False
        for service in services:
            if service.uuid == self.SERVICE_UUID:
                for char in service.characteristics:
                    if char.uuid == self.ACCEL_UUID:
                        found = True
                        break
                if found:
                    break

        if not found:
            print(f"Characteristic {self.ACCEL_UUID} not found")
            return False

        return True

    async def start_notify(self):
        await self.client.start_notify(self.ACCEL_UUID, self.callback)

    async def stop_notify(self):
        await self.client.stop_notify(self.ACCEL_UUID)

    async def disconnect(self):
        await self.client.disconnect()

    # Callback function for when a notification is received.
    def callback(self, sender: int, data: bytearray):
        if not self.HasStarted:
            self.HasStarted = True
            print("1. Has started")

        accelX = int.from_bytes(data[0:2], byteorder='little', signed=True)
        accelY = int.from_bytes(data[2:4], byteorder='little', signed=True)
        accelZ = int.from_bytes(data[4:6], byteorder='little', signed=True)

        gyroX = int.from_bytes(data[6:8], byteorder='little', signed=True)
        gyroY = int.from_bytes(data[8:10], byteorder='little', signed=True)
        gyroZ = int.from_bytes(data[10:12], byteorder='little', signed=True)

        timestamp = int.from_bytes(data[12:], byteorder='little', signed=False)

        if self.IsDebug:
            print(
                f"Time: {timestamp} ms, Accel: ({accelX}, {accelY}, {accelZ}), Gyro: ({gyroX}, {gyroY}, {gyroZ})")

        # self.Timestamps = self.data['Timestamp']
        # self.AccelX = self.data['AccelX']
        # self.AccelY = self.data['AccelY']
        # self.AccelZ = self.data['AccelZ']
        # self.GyroX = self.data['GyroX']
        # self.GyroY = self.data['GyroY']
        # self.GyroZ = self.data['GyroZ']

        self.Timestamps.append(timestamp)
        self.AccelX.append((timestamp, accelX))
        self.AccelY.append((timestamp, accelY))
        self.AccelZ.append((timestamp, accelZ))
        self.GyroX.append((timestamp, gyroX))
        self.GyroY.append((timestamp, gyroY))
        self.GyroZ.append((timestamp, gyroZ))


async def discover_device(device_name_pattern):
    scanner = BleakScanner()
    start_time = loop.time()

    print("Scanning for devices...")

    while True:
        devices = await scanner.discover()

        for device in devices:
            print(f"Found device: {device.name} ({device.address})")
            if device.name and re.search(device_name_pattern, device.name, re.IGNORECASE):
                print(f"Found arduino: {device.name}")
                return device.address

        # Check if 15 seconds have passed
        if loop.time() - start_time > 15:
            print("Device not found. Stopping scan.")
            return None

        # Sleep for a short time before trying again
        await asyncio.sleep(0.5)


async def main(device_name_pattern):
    device_address = await discover_device(device_name_pattern)

    if device_address is None:
        print("Device not found, stopping program.")
        return

    if device_address:
        collector = ArduinoAccelDataCollector(device_address)
        print(f"Connecting to {device_address}...")

        if not await collector.connect():
            return

        print("Connected. Starting data collection...")
        await collector.start_notify()

        print("2. Will sleep")
        await asyncio.sleep(90)  # Collect data for 30 seconds
        print("3. Slept")
        await collector.stop_notify()
        await collector.disconnect()
        print("Disconnected.")

        data = collector.data

        # collector.plot_rolling_means()

        # Export the collected data to a CSV file
        collector.export_to_csv()

        # Plot the collected data
        fig, axs = plt.subplots(2, 3)

        # Assuming that collector.data['Timestamp'] is a list of timestamps and the rest are lists of tuples
        timestamps = collector.data['Timestamp']
        for i, axis in enumerate(['AccelX', 'AccelY', 'AccelZ']):
            # No need to zip since we're not dealing with a list of tuples here
            # Unpack values from tuples
            values = [value for _, value in collector.data[axis]]
            row = i // 3
            col = i % 3
            axs[row, col].plot(timestamps, values)
            axs[row, col].set_title(axis)

        # Repeat the same for gyro data if needed
        for i, axis in enumerate(['GyroX', 'GyroY', 'GyroZ'], start=3):
            # Unpack values from tuples
            values = [value for _, value in collector.data[axis]]
            row = i // 3
            col = i % 3
            axs[row, col].plot(timestamps, values)
            axs[row, col].set_title(axis)

        for ax in axs.flat:
            ax.set(xlabel='time (ms)', ylabel='value')

        plt.tight_layout()
        # plt.show()


# Regex pattern for the Arduino's name
device_name_pattern = "Arduino Acceleromet"
loop = asyncio.get_event_loop()
loop.run_until_complete(main(device_name_pattern))
