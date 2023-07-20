import asyncio
import matplotlib.pyplot as plt
from bleak import BleakClient, BleakScanner
from collections import defaultdict
import re

class ArduinoAccelDataCollector:
    def __init__(self, arduino_address):
        self.address = arduino_address
        self.client = BleakClient(self.address)
        self.data = defaultdict(list)
        self.SERVICE_UUID = "477fcf1c-b91c-4c23-9004-95211c661945"
        self.ACCEL_UUID = "eebf853b-a580-424c-a827-d6600f4253e1"

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
        accelX = int.from_bytes(data[0:2], byteorder='little', signed=True)
        accelY = int.from_bytes(data[2:4], byteorder='little', signed=True)
        accelZ = int.from_bytes(data[4:6], byteorder='little', signed=True)

        gyroX = int.from_bytes(data[6:8], byteorder='little', signed=True)
        gyroY = int.from_bytes(data[8:10], byteorder='little', signed=True)
        gyroZ = int.from_bytes(data[10:12], byteorder='little', signed=True)

        timestamp = int.from_bytes(data[12:], byteorder='little', signed=False)

        print(f"Time: {timestamp} ms, Accel: ({accelX}, {accelY}, {accelZ}), Gyro: ({gyroX}, {gyroY}, {gyroZ})")

        self.data['accelX'].append((timestamp, accelX))
        self.data['accelY'].append((timestamp, accelY))
        self.data['accelZ'].append((timestamp, accelZ))
        self.data['gyroX'].append((timestamp, gyroX))
        self.data['gyroY'].append((timestamp, gyroY))
        self.data['gyroZ'].append((timestamp, gyroZ))


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

        await asyncio.sleep(30) # Collect data for 60 seconds

        await collector.stop_notify()
        await collector.disconnect()
        print("Disconnected.")

        # Plot the collected data
        fig, axs = plt.subplots(2, 3)

        for i, (axis, data) in enumerate(collector.data.items()):
            timestamps, values = zip(*data)
            row = i // 3
            col = i % 3
            axs[row, col].plot(timestamps, values)
            axs[row, col].set_title(axis)

        for ax in axs.flat:
            ax.set(xlabel='time (ms)', ylabel='value')

        plt.tight_layout()
        plt.show()
        
        

device_name_pattern = "Arduino Acceleromet" # Regex pattern for the Arduino's name
loop = asyncio.get_event_loop()
loop.run_until_complete(main(device_name_pattern))