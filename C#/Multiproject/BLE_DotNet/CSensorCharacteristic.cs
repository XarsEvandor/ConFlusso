using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Runtime.InteropServices.WindowsRuntime;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Windows.Devices.Bluetooth.GenericAttributeProfile;
using Windows.Storage.Streams;

namespace BLE_DotNet
{
    internal class CSensorCharacteristic
    {
        private GattCharacteristic __Characteristic;

        private object __lock = new object();

        // .....................................................................................
        private List<int> __valuesX = new List<int>();

        public List<int> ValuesX
        {
            get
            {
                List<int> oValuesReturned = new List<int>();

                //We need to get the UUID of the characteristic later, so we insert it into the first index of the returned list. 
                //oValuesReturned.Add(int.Parse(__Characteristic.Uuid.ToString("N").Substring(4, 4)));
                try
                {
                    lock (__lock)
                    {
                        foreach (int nValue in __valuesX)
                            oValuesReturned.Add(nValue);
                        this.__valuesX.Clear();
                    }

                }
                finally
                {
                }

                return oValuesReturned;
            }

        }
        // .....................................................................................
        private List<int> __valuesY = new List<int>();

        public List<int> ValuesY
        {
            get
            {
                List<int> oValuesReturned = new List<int>();

                //We need to get the UUID of the characteristic later, so we insert it into the first index of the returned list. 
                //oValuesReturned.Add(int.Parse(__Characteristic.Uuid.ToString("N").Substring(4, 4)));
                try
                {
                    lock (__lock)
                    {
                        foreach (int nValue in __valuesY)
                            oValuesReturned.Add(nValue);
                        this.__valuesY.Clear();
                    }

                }
                finally
                {
                }

                return oValuesReturned;
            }

        }
        // .....................................................................................
        private List<int> __valuesZ = new List<int>();

        public List<int> ValuesZ
        {
            get
            {
                List<int> oValuesReturned = new List<int>();

                //We need to get the UUID of the characteristic later, so we insert it into the first index of the returned list. 
                //oValuesReturned.Add(int.Parse(__Characteristic.Uuid.ToString("N").Substring(4, 4)));
                try
                {
                    lock (__lock)
                    {
                        foreach (int nValue in __valuesZ)
                            oValuesReturned.Add(nValue);
                        this.__valuesZ.Clear();
                    }

                }
                finally
                {
                }

                return oValuesReturned;
            }

        }
        // .....................................................................................



        private Thread __thread;

        public CSensorCharacteristic(GattCharacteristic p_oCharacteristic)
        {
            this.__Characteristic = p_oCharacteristic;

            //__thread = new Thread(ThreadRunOnce);
            //__thread.Start();
        }


        public async void ThreadRunOnce()
        {

            ////Console.WriteLine(characteristic.Uuid.ToString());
            //GattCharacteristicProperties properties = __Characteristic.CharacteristicProperties;

            //if (properties.HasFlag(GattCharacteristicProperties.Notify))
            //{
            //    GattCommunicationStatus status = await __Characteristic.WriteClientCharacteristicConfigurationDescriptorAsync(
            //        GattClientCharacteristicConfigurationDescriptorValue.Notify);
            //    if (status == GattCommunicationStatus.Success)
            //    {
            //        __Characteristic.ValueChanged += Characteristic_ValueChanged;
            //        Console.WriteLine($"Subscribed to characteristic: {__Characteristic.Uuid}");
            //        // Server has been informed of clients interest.
            //    }
            //}


            // initialize status
            GattCommunicationStatus status = GattCommunicationStatus.Unreachable;
            var cccdValue = GattClientCharacteristicConfigurationDescriptorValue.None;
            if (__Characteristic.CharacteristicProperties.HasFlag(GattCharacteristicProperties.Indicate))
            {
                cccdValue = GattClientCharacteristicConfigurationDescriptorValue.Indicate;
            }
            else if (__Characteristic.CharacteristicProperties.HasFlag(GattCharacteristicProperties.Notify))
            {
                cccdValue = GattClientCharacteristicConfigurationDescriptorValue.Notify;
            }

            try
            {
                // BT_Code: Must write the CCCD in order for server to send indications.
                // We receive them in the ValueChanged event handler.
                GattCommunicationStatus gattCommunicationStatus = await __Characteristic.WriteClientCharacteristicConfigurationDescriptorAsync(cccdValue);
                status = gattCommunicationStatus;

                if (status == GattCommunicationStatus.Success)
                {
                    __Characteristic.ValueChanged += Characteristic_ValueChanged;

                    //rootPage.NotifyUser("Successfully subscribed for value changes", NotifyType.StatusMessage);
                    Console.WriteLine($"Subscribed to characteristic: {__Characteristic.Uuid}");
                }
                else
                {
                    //rootPage.NotifyUser($"Error registering for value changes: {status}", NotifyType.ErrorMessage);
                    Console.WriteLine($"Error registering for value changes: {status}");
                }
            }
            catch (Exception ex)
            {
                // This usually happens when a device reports that it support indicate, but it actually doesn't.
                //rootPage.NotifyUser(ex.Message, NotifyType.ErrorMessage);
                Console.WriteLine(ex.Message);
            }

        }


        public async Task SubscribeToNotifications()
        {

            ////Console.WriteLine(characteristic.Uuid.ToString());
            //GattCharacteristicProperties properties = __Characteristic.CharacteristicProperties;

            //if (properties.HasFlag(GattCharacteristicProperties.Notify))
            //{
            //    GattCommunicationStatus status = await __Characteristic.WriteClientCharacteristicConfigurationDescriptorAsync(
            //        GattClientCharacteristicConfigurationDescriptorValue.Notify);
            //    if (status == GattCommunicationStatus.Success)
            //    {
            //        __Characteristic.ValueChanged += Characteristic_ValueChanged;
            //        Console.WriteLine($"Subscribed to characteristic: {__Characteristic.Uuid}");
            //        // Server has been informed of clients interest.
            //    }
            //}


            // initialize status
            GattCommunicationStatus status = GattCommunicationStatus.Unreachable;
            var cccdValue = GattClientCharacteristicConfigurationDescriptorValue.None;
            if (__Characteristic.CharacteristicProperties.HasFlag(GattCharacteristicProperties.Indicate))
            {
                cccdValue = GattClientCharacteristicConfigurationDescriptorValue.Indicate;
            }
            else if (__Characteristic.CharacteristicProperties.HasFlag(GattCharacteristicProperties.Notify))
            {
                cccdValue = GattClientCharacteristicConfigurationDescriptorValue.Notify;
            }

            try
            {
                // BT_Code: Must write the CCCD in order for server to send indications.
                // We receive them in the ValueChanged event handler.
                status = await __Characteristic.WriteClientCharacteristicConfigurationDescriptorAsync(cccdValue);

                if (status == GattCommunicationStatus.Success)
                {
                    __Characteristic.ValueChanged += Characteristic_ValueChanged;
                    //rootPage.NotifyUser("Successfully subscribed for value changes", NotifyType.StatusMessage);
                    Console.WriteLine($"Subscribed to characteristic: {__Characteristic.Uuid}");
                }
                else
                {
                    //rootPage.NotifyUser($"Error registering for value changes: {status}", NotifyType.ErrorMessage);
                    Console.WriteLine($"Error registering for value changes: {status}");
                }
            }
            catch (Exception ex)
            {
                // This usually happens when a device reports that it support indicate, but it actually doesn't.
                //rootPage.NotifyUser(ex.Message, NotifyType.ErrorMessage);
                Console.WriteLine(ex.Message);
            }

        }


        private void Characteristic_ValueChanged(GattCharacteristic sender, GattValueChangedEventArgs args)
        {
            // An Indicate or Notify reported that the value has changed.
            DataReader reader = DataReader.FromBuffer(args.CharacteristicValue);
            byte[] sBytes = new byte[20];
            reader.ReadBytes(sBytes);


            int nX =  sBytes[1]* 256 + sBytes[0];
            int nY = sBytes[3] * 256 + sBytes[2];
            int nZ = sBytes[5] * 256 + sBytes[4];
            int nGyroX = sBytes[7] * 256 + sBytes[6];
            int nGyroY = sBytes[9] * 256 + sBytes[8];
            int nGyroZ = sBytes[11] * 256 + sBytes[10];

            Console.WriteLine(nX.ToString() + "," + nY.ToString() + "," + nZ.ToString() + "   "
                            + nGyroX.ToString() + "," + nGyroY.ToString() + "," + nGyroZ.ToString());
            

            //string sData = Encoding.ASCII.GetString(sBytes, 0, 5);
            //Console.WriteLine(sData);

            //var value = reader.ReadBuffer(20).ToArray();



            //Console.WriteLine($"{value}");
            //__values.Add(value);

        }
    }
}
