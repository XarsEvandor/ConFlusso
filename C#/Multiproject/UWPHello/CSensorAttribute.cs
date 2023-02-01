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
        private object __lock = new object();
        private List<float> __values = new List<float>();
        public List<float> Values
        {   get 
            {
                List<float> oValuesReturned = new List<float>();
                try
                {
                    lock (__lock)
                    {
                        foreach (float nValue in __values)
                            oValuesReturned.Add(nValue);
                        this.__values.Clear();
                    }
                    
                }
                finally
                {
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
            try
            {
                var device = await Windows.Devices.Enumeration.DeviceInformation.FindAllAsync(Windows.Devices.Bluetooth.BluetoothLEDevice.GetDeviceSelectorFromDeviceName("Arduino Accelerometer")).AsTask();
                var bleDevice = await Windows.Devices.Bluetooth.BluetoothLEDevice.FromIdAsync(device.First().Id);

                // Get service and characteristics by UUID
                var gattAsyncServiceResult = await bleDevice.GetGattServicesForUuidAsync(new Guid(this.__serviceGUID));
                if (gattAsyncServiceResult.Status == GattCommunicationStatus.Success)
                {
                    __service = gattAsyncServiceResult.Services.FirstOrDefault();
                }
                else
                {
                    System.Diagnostics.Debug.WriteLine("Unable to get service.");
                }

                var gattAsyncCharacteristicResult = await __service.GetCharacteristicsForUuidAsync(new Guid(this.__characteristicGUID));
                if (gattAsyncCharacteristicResult.Status == GattCommunicationStatus.Success)
                {
                    __characteristic = gattAsyncCharacteristicResult.Characteristics.FirstOrDefault();
                }

                __characteristic.ValueChanged += ValueChanged;

                await __characteristic.WriteClientCharacteristicConfigurationDescriptorAsync(GattClientCharacteristicConfigurationDescriptorValue.Notify);
            }
            catch (Exception ex)
            {
                // Handle the exception here, for example by logging it.
                System.Diagnostics.Debug.WriteLine("An exception occurred during initialization: " + ex.Message);
            }
        }

        private void ValueChanged(GattCharacteristic sender, GattValueChangedEventArgs args)
        {
          
            // Get value from args
            var data = new byte[args.CharacteristicValue.Length];
            DataReader.FromBuffer(args.CharacteristicValue).ReadBytes(data);

            // Convert value to float
            float nValue = BitConverter.ToSingle(data, 0);

            __values.Add(nValue);
        }

    }
}
