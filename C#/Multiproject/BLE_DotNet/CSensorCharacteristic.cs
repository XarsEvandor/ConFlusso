using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Windows.Devices.Bluetooth.GenericAttributeProfile;
using Windows.Storage.Streams;

namespace BLE_DotNet
{
    internal class CSensorCharacteristic
    {
        private GattCharacteristic __Characteristic;

        private object __lock = new object();
        private List<int> __values = new List<int>();
        public List<int> Values
        {
            get
            {
                List<int> oValuesReturned = new List<int>();

                //We need to get the UUID of the characteristic later, so we insert it into the first index of the returned list.
                oValuesReturned.Add(int.Parse(__Characteristic.Uuid.ToString()));
                try
                {
                    lock (__lock)
                    {
                        foreach (int nValue in __values)
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

        public CSensorCharacteristic(GattCharacteristic p_oCharacteristic)
        {
            this.__Characteristic = p_oCharacteristic;
        }

        public async Task SubscribeToNotifications()
        {
            
            //Console.WriteLine(characteristic.Uuid.ToString());
            GattCharacteristicProperties properties = __Characteristic.CharacteristicProperties;

            if (properties.HasFlag(GattCharacteristicProperties.Notify))
            {
                GattCommunicationStatus status = await __Characteristic.WriteClientCharacteristicConfigurationDescriptorAsync(
                    GattClientCharacteristicConfigurationDescriptorValue.Notify);
                if (status == GattCommunicationStatus.Success)
                {
                    __Characteristic.ValueChanged += Characteristic_ValueChanged;
                    Console.WriteLine($"Subscribed to characteristic: {__Characteristic.Uuid}");
                    // Server has been informed of clients interest.
                }
            }
               
        }


        private void Characteristic_ValueChanged(GattCharacteristic sender, GattValueChangedEventArgs args)
        {
            // An Indicate or Notify reported that the value has changed.
            var reader = DataReader.FromBuffer(args.CharacteristicValue);
            var value = reader.ReadByte();

            //Console.WriteLine($"{value}");
            __values.Add(value);
        }
    }
}
