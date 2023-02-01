using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Windows.Devices.Bluetooth.GenericAttributeProfile;
using Windows.Storage.Streams;

namespace BLE_Data_Receiver
{
    public class CSensorAttribute
    {
        private GattDeviceService  __service;
        private GattCharacteristic __characteristic;
        private List<float> __values = new List<float>();
        private bool __isReadingValues = false;
        public List<float> Values
        {   get 
            {
                List<float> oValuesReturned = new List<float>();
                try
                {
                    __isReadingValues = true;
                    foreach (float nValue in __values)
                        oValuesReturned.Add(nValue);
                    this.__values.Clear();
                }
                finally
                {
                    __isReadingValues = false;
                }

                return oValuesReturned;  
            } 
        
        }
        private String __serviceGUID;
        private String __characteristicGUID;


        public CSensorAttribute(string p_sServiceGUID, string p_sCharacteristicGUID)
        {
            this.__serviceGUID = p_sServiceGUID;
            this.__characteristicGUID = p_sCharacteristicGUID;
        }

        public async void Initialize()
        {
            var device = await Windows.Devices.Enumeration.DeviceInformation.FindAllAsync(Windows.Devices.Bluetooth.BluetoothLEDevice.GetDeviceSelectorFromDeviceName("Arduino Accelerometer and Gyroscope")).AsTask();
            var bleDevice = await Windows.Devices.Bluetooth.BluetoothLEDevice.FromIdAsync(device.First().Id);

            // Get service and characteristics by UUID
            __service = bleDevice.GetGattService(new Guid(this.__serviceGUID));
            __characteristic = __service.GetCharacteristics(new Guid(this.__characteristicGUID)).First();
            __characteristic.ValueChanged += ValueChanged;

            await __characteristic.WriteClientCharacteristicConfigurationDescriptorAsync(GattClientCharacteristicConfigurationDescriptorValue.Notify);
        }

        private void ValueChanged(GattCharacteristic sender, GattValueChangedEventArgs args)
        {
            while (__isReadingValues)
                Thread.Sleep(1);

            // Get value from args
            var data = new byte[args.CharacteristicValue.Length];
            DataReader.FromBuffer(args.CharacteristicValue).ReadBytes(data);

            // Convert value to float
            float nValue = BitConverter.ToSingle(data, 0);

            __values.Add(nValue);
        }

    }
}
