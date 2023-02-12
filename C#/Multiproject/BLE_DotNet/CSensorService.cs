﻿using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Windows.Devices.Bluetooth.GenericAttributeProfile;

namespace BLE_DotNet
{
    internal class CSensorService
    {
        private GattDeviceService __Service;
        public Dictionary<string, CSensorCharacteristic> dCharacteristicsUUIDs = new Dictionary<string, CSensorCharacteristic>();

        public CSensorService(GattDeviceService p_oService)
        { 
            this.__Service = p_oService;
        }

        public async Task GetServiceCharacteristics()
        {
            GattCharacteristicsResult oCharacteristicsResult = await __Service.GetCharacteristicsAsync();

            if (oCharacteristicsResult.Status == GattCommunicationStatus.Success)
            {
                var oCharacteristics = oCharacteristicsResult.Characteristics;
                foreach (var characteristic in oCharacteristics)
                {
                    Console.WriteLine(characteristic.Uuid.ToString());
                }
            }
        }

        public async Task SubscribeToCharNotifications()
        {
            Console.WriteLine($"\nFound Service: {__Service.Uuid}.\n");
            GattCharacteristicsResult oCharacteristicsResult = await __Service.GetCharacteristicsAsync();

            if (oCharacteristicsResult.Status == GattCommunicationStatus.Success)
            {
                var oCharacteristics = oCharacteristicsResult.Characteristics;
                
                foreach (var characteristic in oCharacteristics)
                {
                    CSensorCharacteristic oSensorCharacteristic = new CSensorCharacteristic(characteristic);
                    await oSensorCharacteristic.SubscribeToNotifications();
                    dCharacteristicsUUIDs.Add(characteristic.Uuid.ToString(), oSensorCharacteristic);
                }
            }
                    
        }
    }
}
