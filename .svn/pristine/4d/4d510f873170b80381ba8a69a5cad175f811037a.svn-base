using System;
using Windows.Devices.Enumeration;
using Windows.Devices.Bluetooth.Advertisement;
using System.Diagnostics;
using System.IO;

using System.Collections.Generic;
using System.Collections.ObjectModel;
using Windows.Devices.Bluetooth;
using Windows.UI.Core;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Navigation;




namespace UWPHello
{
    public class CDeviceWatcher
    {
        // Additional properties we would like about the device.
        // Property strings are documented here https://msdn.microsoft.com/en-us/library/windows/desktop/ff521659(v=vs.85).aspx
        private static string[] requestedProperties = { "System.Devices.Aep.DeviceAddress", "System.Devices.Aep.IsConnected", "System.Devices.Aep.Bluetooth.Le.IsConnectable" };

        // BT_Code: Example showing paired and non-paired in a single query.
        private static string aqsAllBluetoothLEDevices = "(System.Devices.Aep.ProtocolId:=\"{bb7bb05e-5972-42b5-94fc-76eaa7084d49}\")";

        public static async void EnumerateDevicesAsync()
        {
            BluetoothLEAdvertisementWatcher watcher = new BluetoothLEAdvertisementWatcher();
            watcher.Received += (w, a) =>
            {
                Debug.WriteLine("Device Name: " + a.BluetoothAddress);

                foreach(var UUID in a.Advertisement.ServiceUuids)
                {
                    Debug.WriteLine($"{UUID}");
                }

                Debug.WriteLine("Device Id: " + a.Advertisement.LocalName);
            };
            watcher.Start();

        }


        private DeviceInformation __arduinoDeviceInfo = null;
        public DeviceInformation ArduinoDeviceInfo { get { return __arduinoDeviceInfo; } }



        public CDeviceWatcher()
        {
            DeviceWatcher deviceWatcher =
                    DeviceInformation.CreateWatcher(
                        aqsAllBluetoothLEDevices,
                        requestedProperties,
                        DeviceInformationKind.AssociationEndpoint);

            // Register event handlers before starting the watcher.
            deviceWatcher.Added += this.DeviceWatcher_Added;
            deviceWatcher.Updated += this.DeviceWatcher_Updated;
            deviceWatcher.Removed += this.DeviceWatcher_Removed;
            deviceWatcher.EnumerationCompleted += this.DeviceWatcher_EnumerationCompleted;
            deviceWatcher.Stopped += this.DeviceWatcher_Stopped;

            // Start over with an empty collection.
            //KnownDevices.Clear();

            // Start the watcher. Active enumeration is limited to approximately 30 seconds.
            // This limits power usage and reduces interference with other Bluetooth activities.
            // To monitor for the presence of Bluetooth LE devices for an extended period,
            // use the BluetoothLEAdvertisementWatcher runtime class. See the BluetoothAdvertisement
            // sample for an example.
            deviceWatcher.Start();
        }

        private async void DeviceWatcher_Added(DeviceWatcher sender, DeviceInformation deviceInfo)
        {
            Debug.WriteLine(deviceInfo.Id);
            if (deviceInfo.Name == "Arduino Accelerometer")
            {
                __arduinoDeviceInfo = deviceInfo;
            }
        }

        private async void DeviceWatcher_Updated(DeviceWatcher sender, DeviceInformationUpdate deviceInfoUpdate)
        {
            Debug.WriteLine("Updated");
        }

        private async void DeviceWatcher_Removed(DeviceWatcher sender, DeviceInformationUpdate deviceInfoUpdate)
        {
            Debug.WriteLine("Removed");
        }

        private async void DeviceWatcher_EnumerationCompleted(DeviceWatcher sender, object e)
        {
            Debug.WriteLine("EnumerationCompleted");
        }

        private async void DeviceWatcher_Stopped(DeviceWatcher sender, object e)
        {
            Debug.WriteLine("Stopped");
        }
    }
}
