from collections import defaultdict
import pandas as pd


class Characteristic:
    def __init__(self, characteristicUUID, client):
        self.characteristicUUID = characteristicUUID
        self.client = client
        self.data = defaultdict(list)
        self.IsDebug = False
        
    async def start_notify(self):
        await self.client.start_notify(self.characteristicUUID, self.callback)

    async def stop_notify(self):
        await self.client.stop_notify(self.characteristicUUID)
    
    # Callback function for when a notification is received. 
    def callback(self, sender: int, data: bytearray):
        heading = int.from_bytes(data[0:2], byteorder='little', signed=True)
        pitch = int.from_bytes(data[2:4], byteorder='little', signed=True)
        roll = int.from_bytes(data[4:6], byteorder='little', signed=True)
        timestamp = int.from_bytes(data[12:], byteorder='little', signed=False)

        if self.IsDebug:
            print(f"Time: {timestamp} ms, Orientation: Heading={heading}, Pitch={pitch}, Roll={roll}")

        # self.data['time'].append(timestamp)
        self.data['heading'].append((timestamp, heading))
        self.data['pitch'].append((timestamp, pitch))
        self.data['roll'].append((timestamp, roll))
        
    def getDataFrame(self):
        return pd.DataFrame.from_dict(self.data)
        
        
    