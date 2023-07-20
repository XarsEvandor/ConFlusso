from CNotifyChar import Characteristic


class Service:
    def __init__(self, serviceUUID, characteristicUUID, client, service):
        self.serviceUUID = serviceUUID
        self.characteristicUUID = characteristicUUID
        self.client = client
        self.service = service
        self.characteristics = []
        
    def getServiceUUID(self):
        return self.serviceUUID
    
    async def getCharacteristics(self):  
        found = False
        for char in self.service.characteristics:
            if char.uuid in self.characteristicUUID:
                characteristic = Characteristic(char.uuid, self.client)
                await characteristic.start_notify()
                self.characteristics.append(characteristic)
                found = True
        
        if not found:
            print(f"No characteristics found.")
            return False
                
        
    
        