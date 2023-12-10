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
        self.Heading = self.data['Heading']
        self.Pitch = self.data['Pitch']
        self.Roll = self.data['Roll']

        self.SERVICE_UUID = "477fcf1c-b91c-4c23-9004-95211c661945"
        self.ACCEL_UUID = "eebf853b-a580-424c-a827-d6600f4253e1"
        self.IsDebug = True
        self.HasStarted = False

    def plot_data(self):
        plt.figure(figsize=(15, 5))
        plt.plot(self.Timestamps, [h[1] for h in self.Heading], label='Heading')
        plt.plot(self.Timestamps, [p[1] for p in self.Pitch], label='Pitch')
        plt.plot(self.Timestamps, [r[1] for r in self.Roll], label='Roll')
        plt.title('Orientation Data Over Time')
        plt.xlabel('Timestamp')
        plt.ylabel('Degrees')
        plt.legend()
        plt.grid(True)
        plt.show()

    def export_to_csv(self, filename="orientation_data.csv"):
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Timestamp", "Heading", "Pitch", "Roll"])

            length = min(len(self.Timestamps), len(self.Heading), len(self.Pitch), len(self.Roll))
            for i in range(length):
                csv_writer.writerow([self.Timestamps[i], self.Heading[i][1], self.Pitch[i][1], self.Roll[i][1]])

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

    def callback(self, sender: int, data: bytearray):
        if not self.HasStarted:
            self.HasStarted = True
            print("1. Has started")

        heading = int.from_bytes(data[0:2], byteorder='little', signed=True)
        pitch = int.from_bytes(data[2:4], byteorder='little', signed=True)
        roll = int.from_bytes(data[4:6], byteorder='little', signed=True)
        timestamp = int.from_bytes(data[12:], byteorder='little', signed=False)

        if self.IsDebug:
            print(f"Time: {timestamp} ms, Orientation: Heading={heading}, Pitch={pitch}, Roll={roll}")

        self.Timestamps.append(timestamp)
        self.Heading.append((timestamp, heading))
        self.Pitch.append((timestamp, pitch))
        self.Roll.append((timestamp, roll))

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

        if loop.time() - start_time > 15:
            print("Device not found. Stopping scan.")
            return None

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

        await asyncio.sleep(30)  # Collect data for 30 seconds
        await collector.stop_notify()
        await collector.disconnect()
        print("Disconnected.")

        # Optional: Plot the collected data
        collector.plot_data()

        # Export the collected data to a CSV file
        collector.export_to_csv()

# Regex pattern for the Arduino's name
device_name_pattern = "Arduino Acceleromet"
loop = asyncio.get_event_loop()
loop.run_until_complete(main(device_name_pattern))
