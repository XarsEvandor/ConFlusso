using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Windows.Devices.Bluetooth;
using Windows.Devices.Bluetooth.GenericAttributeProfile;

namespace BLE_DotNet
{
    internal class CSensor
    {
        private BluetoothLEDevice __Device;
        public CSensorService oService;

        public CSensor(BluetoothLEDevice p_oDevice) 
        { 
            __Device = p_oDevice; 
        }

        public async Task GetSensorServices()
        {
            GattDeviceServicesResult oServicesResult = await __Device.GetGattServicesAsync();

            if (oServicesResult.Status == GattCommunicationStatus.Success)
            {
                Console.WriteLine("\nSuccessfuly paired with device.\n Displaying service UUIDs: \n");

                var services = oServicesResult.Services;
                foreach (var service in services)
                {
                    Console.WriteLine(service.Uuid.ToString());
                }
            }

        }

        public async Task SubscribeToServiceCharsNotifications(string p_sServiceUUID, List<string> p_lsCharacteristicsUUIDs)
        {
            GattDeviceServicesResult oServicesResult = await __Device.GetGattServicesAsync();

            if (oServicesResult.Status == GattCommunicationStatus.Success)
            {
                Console.WriteLine("\nSuccessfuly paired with device.");

                var services = oServicesResult.Services;
                foreach (var service in services)
                {
                    if(service.Uuid.ToString().Contains(p_sServiceUUID)) 
                    { 
                        oService = new CSensorService(service);
                        await oService.SubscribeToCharNotifications(p_lsCharacteristicsUUIDs);
                    }
                }
            }
        }

    
    }
}
