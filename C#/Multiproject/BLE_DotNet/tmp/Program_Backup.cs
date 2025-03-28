﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using Windows.Devices.Bluetooth;
using Windows.Devices.Bluetooth.GenericAttributeProfile;
using Windows.Devices.Enumeration;
using Windows.Storage.Streams;

namespace BLE_DotNet
{
    internal class Program_Backup
    {
        static DeviceInformation oDeviceInfo = null;
        private static string p_sAccelUuid = "1101";
        //private static bool fEnumerationComplete = false;

        static async Task Main_not(string[] args)
        {
            // Query for extra properties you want returned
            string[] requestedProperties = { "System.Devices.Aep.DeviceAddress", "System.Devices.Aep.IsConnected" };

            DeviceWatcher deviceWatcher =
                        DeviceInformation.CreateWatcher(
                                BluetoothLEDevice.GetDeviceSelectorFromPairingState(false),
                                requestedProperties,
                                DeviceInformationKind.AssociationEndpoint);

            // Register event handlers before starting the watcher.
            // Added, Updated and Removed are required to get all nearby devices
            deviceWatcher.Added += DeviceWatcher_Added;
            deviceWatcher.Updated += DeviceWatcher_Updated;
            deviceWatcher.Removed += DeviceWatcher_Removed;

            // EnumerationCompleted and Stopped are optional to implement.
            deviceWatcher.EnumerationCompleted += DeviceWatcher_EnumerationCompleted;
            deviceWatcher.Stopped += DeviceWatcher_Stopped;

            // Start the watcher.
            deviceWatcher.Start();

            while (true)
            {
                if(oDeviceInfo == null)
                {
                    Thread.Sleep(200);
                    //if (fEnumerationComplete)
                    //{
                    //    Console.WriteLine("Enumeration Complete");
                    //    deviceWatcher.Stop();
                    //    Thread.Sleep(200);
                    //    deviceWatcher.Start();
                    //    fEnumerationComplete = false;
                    //}
                }
                else
                {
                    //Console.WriteLine("Press any key to pair with " + oDeviceInfo.Name + ".");
                    //Console.ReadKey();
                    BluetoothLEDevice bluetoothLeDevice = await BluetoothLEDevice.FromIdAsync(oDeviceInfo.Id);
                    Console.WriteLine("\nPairing...");

                    GattDeviceServicesResult oServicesResult = await bluetoothLeDevice.GetGattServicesAsync();

                    if (oServicesResult.Status == GattCommunicationStatus.Success)
                    {
                        Console.WriteLine("\nSuccessfuly paired with device.\n Displaying service UUIDs: \n");
                        var services = oServicesResult.Services;
                        foreach(var service in services)
                        {
                            Console.WriteLine(service.Uuid.ToString());

                            if(service.Uuid.ToString("N").Substring(4,4) == p_sAccelUuid)
                            {
                                Console.WriteLine("\nFound Accelerometer Service.\n Displaying characteristics UUIDs: \n");
                                GattCharacteristicsResult oCharacteristicsResult = await service.GetCharacteristicsAsync();

                                if (oCharacteristicsResult.Status == GattCommunicationStatus.Success)
                                {
                                    var oCharacteristics = oCharacteristicsResult.Characteristics;
                                    foreach (var characteristic in oCharacteristics)
                                    {
                                        Console.WriteLine(characteristic.Uuid.ToString());
                                        GattCharacteristicProperties properties = characteristic.CharacteristicProperties;

                                        if (properties.HasFlag(GattCharacteristicProperties.Notify) && characteristic.Uuid.ToString().Contains("2101"))
                                        {
                                            GattCommunicationStatus status = await characteristic.WriteClientCharacteristicConfigurationDescriptorAsync(
                                                GattClientCharacteristicConfigurationDescriptorValue.Notify);
                                            if (status == GattCommunicationStatus.Success)
                                            {
                                                characteristic.ValueChanged += Characteristic_ValueChanged;
                                                // Server has been informed of clients interest.
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }

                    Console.WriteLine("Press any key to exit");
                    Console.ReadKey();
                    break;
                }

            }

            deviceWatcher.Stop();
        }

        private static void Characteristic_ValueChanged(GattCharacteristic sender, GattValueChangedEventArgs args)
        {
            // An Indicate or Notify reported that the value has changed.
            var reader = DataReader.FromBuffer(args.CharacteristicValue);
            var value = reader.ReadByte();

            Console.WriteLine($"{value}");
        }

        private static void DeviceWatcher_Stopped(DeviceWatcher sender, object args)
        {
            //throw new NotImplementedException();
        }

        private static void DeviceWatcher_EnumerationCompleted(DeviceWatcher sender, object args)
        {
            //throw new NotImplementedException();
            //fEnumerationComplete = true;
            //Console.WriteLine("Tis Complete");
        }

        private static void DeviceWatcher_Removed(DeviceWatcher sender, DeviceInformationUpdate args)
        {
            //throw new NotImplementedException();
        }

        private static void DeviceWatcher_Updated(DeviceWatcher sender, DeviceInformationUpdate args)
        {
            //throw new NotImplementedException();
        }

        private static void DeviceWatcher_Added(DeviceWatcher sender, DeviceInformation args)
        {
            Console.WriteLine("Device found: " + args.Name.ToString());
            if (Regex.IsMatch(args.Name, "Arduino\\s+Accelerome", RegexOptions.IgnoreCase))
            {
                oDeviceInfo = args;
            }

        }
    }
}
