import asyncio
import re
from bleak import BleakClient, BleakScanner
from asyncore import loop
from CService import Service


class Device:
    def __init__(self, deviceName, serviceUUID, characteristicUUID, address, client):
        self.deviceName = deviceName
        self.serviceUUID = serviceUUID
        self.characteristicUUID = characteristicUUID 
        self.address = address
        self.client = client
        self.services = []

    # We cannot make the constructor async, so we use a class method to create an instance of the class
    @classmethod
    async def create(cls, deviceName, serviceUUID, characteristicUUID):
        address = await cls.discover_device(deviceName)
        if address is None:
            print("Device not found.")
            return None
        client = BleakClient(address)
        instance = cls(deviceName, serviceUUID, characteristicUUID, address, client)
        if await instance.connect():
            print(f"Connected to {deviceName}. Starting data collection...")
        return instance
        
    def getDeviceName(self):
        return self.deviceName
    
    async def connect(self):
        print(f"Connecting to {self.deviceName}...")

        if not await self.client.connect():
            print(f"Failed to connect to {self.address}")
            return False

        services = self.client.services
        if not services:
            print("No BLE services found")
            return False
        
        found = False
        for service in services:
            if service.uuid in self.serviceUUID:
                oService = Service(self.serviceUUID, self.characteristicUUID, self.client, service)
                await oService.getCharacteristics()
                self.services.append(oService)
                found = True
                    
        if not found:
            print(f"No services found.")
            return False

        return True
    
    
    async def disconnect(self):
        await self.client.disconnect()
    
    @staticmethod
    async def discover_device(deviceName):
        scanner = BleakScanner()
        start_time = asyncio.get_event_loop().time() 
        
        print("Scanning for devices...")

        while True:
            devices = await scanner.discover()

            for device in devices:
                print(f"Found device: {device.name} ({device.address})")
                if device.name and re.search(deviceName, device.name, re.IGNORECASE):
                    print(f"Found arduino: {device.name}")
                    return device.address

            # Check if 15 seconds have passed
            if asyncio.get_event_loop().time() - start_time > 15:  
                print("Device not found. Stopping scan.")
                return None

            # Sleep for a short time before trying again
            await asyncio.sleep(0.5)
