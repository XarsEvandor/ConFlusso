from collections import defaultdict
import pandas as pd


class Characteristic:
    def __init__(self, characteristicUUID, client):
        self.characteristicUUID = characteristicUUID
        self.client = client
        self.data = defaultdict(list)
        
    async def start_notify(self):
        await self.client.start_notify(self.characteristicUUID, self.callback)

    async def stop_notify(self):
        await self.client.stop_notify(self.characteristicUUID)
    
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
        
    def getDataFrame(self):
        return pd.DataFrame.from_dict(self.data)
        
        
    