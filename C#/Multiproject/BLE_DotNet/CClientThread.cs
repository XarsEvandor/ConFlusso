﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Diagnostics;
using Windows.Devices.Enumeration;
using Windows.Devices.Bluetooth;
using Windows.Devices.Bluetooth.GenericAttributeProfile;

namespace BLE_DotNet
{
    public class CClientThread
    {

        private bool __isStarted = false;
        private Thread __thread;
        private int __threadSleepMSecs = 100;
        private bool __continue = true;
        private DeviceInformation DeviceInfo;
        private CSensor Sensor;
        private string AccelUUID;// = "1101";
        private List<string> CharacteristicsUUIDs; //= new List<string> { "2101", "2102", "2103", "2104", "2105", "2106" };

        // Singleton
        private static CClientThread __instance = null;
        public static CClientThread Instance(DeviceInformation p_oDeviceInfo, string p_sAccelUUID, List<string> p_oCharacteristicsUUIDs)
        {
            if (__instance == null)
                __instance = new CClientThread(p_oDeviceInfo, p_sAccelUUID, p_oCharacteristicsUUIDs);
            return __instance;
        }

        public CClientThread(DeviceInformation p_oDeviceInfo, string p_sAccelUUID, List<string> p_oCharacteristicsUUIDs)
        {
            DeviceInfo = p_oDeviceInfo;
            this.AccelUUID = p_sAccelUUID;
            this.CharacteristicsUUIDs = p_oCharacteristicsUUIDs;

            __thread = new Thread(ThreadLoop);
        }

        public void Start()
        {
            if (!__isStarted)
                __thread.Start();
        }

        public void Stop()
        {
            __continue = false;
        }

        public async void ThreadLoop()
        {
            Thread.Sleep(1000);
            // Start
            Debug.WriteLine("Entering thread loop");

            BluetoothLEDevice bluetoothLeDevice = await BluetoothLEDevice.FromIdAsync(DeviceInfo.Id);
            Console.WriteLine("\nPairing...");

            Sensor = new CSensor(bluetoothLeDevice);
            await Sensor.SubscribeToServiceCharsNotifications(AccelUUID, CharacteristicsUUIDs);


            List<int> valuesX;
            List<int> valuesY;
            List<int> valuesZ;

            while (__continue)
            {
                try
                {
                    do
                    {
                        valuesX = Sensor.oService.dCharacteristicsUUIDs["2101"].tempValues;
                        valuesY = Sensor.oService.dCharacteristicsUUIDs["2102"].tempValues;
                        valuesZ = Sensor.oService.dCharacteristicsUUIDs["2103"].tempValues;

                        for (int i = 0; i < valuesX.Count; i++)
                        {
                            Debug.WriteLine($"Accel X: {valuesX[i]} | Accel Y: {valuesY[i]} | Accel Z: {valuesZ[i]}\n");
                            Thread.Sleep(100);
                        }
                    }
                    while (valuesX.Count < 400);

                }
                catch   // Suppress exception
                {
                    Debug.WriteLine("Waiting for device data..." );
                    Thread.Sleep(500);
                }

                Thread.Sleep(__threadSleepMSecs);
            }

            // Stop

        }

    }
}
