using System;
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
    internal class Program
    {
        static DeviceInformation oDeviceInfo = null;
        private static string p_sAccelUuid = "1101";
        private static List<string> p_lsCharacteristicsUUIDs = new List<string> { "2101", "2102", "2103", "2104", "2105", "2106"};
        private static CSensor oSensor;

        //private static bool fEnumerationComplete = false;

        static async Task Main(string[] args)
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
                }
                else
                {
                    BluetoothLEDevice bluetoothLeDevice = await BluetoothLEDevice.FromIdAsync(oDeviceInfo.Id);
                    Console.WriteLine("\nPairing...");

                    oSensor = new CSensor(bluetoothLeDevice);
                    await oSensor.SubscribeToServiceCharsNotifications(p_sAccelUuid, p_lsCharacteristicsUUIDs);

                    for (int i = 0; i < 1000; i++)
                    {
                        deviceWatcher.Stop();
                        await Task.Delay(100);
                        if (deviceWatcher.Status == DeviceWatcherStatus.Stopped)
                        {
                            break;
                        }
                    }
                    List<int> valuesX;
                    List<int> valuesY;
                    List<int> valuesZ;

                    while (true)
                    {
                        try
                        {
                            do
                            {
                                valuesX = oSensor.oService.dCharacteristicsUUIDs["2101"].tempValues;
                                valuesY = oSensor.oService.dCharacteristicsUUIDs["2102"].tempValues;
                                valuesZ = oSensor.oService.dCharacteristicsUUIDs["2103"].tempValues;

                                for (int i = 0; i < valuesX.Count; i++)
                                {
                                    Console.WriteLine($"Accel X: {valuesX[i]} | Accel Y: {valuesY[i]} | Accel Z: {valuesZ[i]}\n");
                                    Thread.Sleep(100);
                                }
                            }
                            while (valuesX.Count < 400);
                           
                        }
                        catch (Exception ex)
                        {
                            Console.WriteLine("Waiting for device data...");
                            Thread.Sleep(500);
                        }
                    }
                   
                }

            }
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
