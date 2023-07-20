using System;
using System.Linq;
using Windows.Devices.Bluetooth.GenericAttributeProfile;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;

public sealed partial class MainPage : Page
{
    private GattDeviceService _service;
    private GattCharacteristic _accelXChar;
    private GattCharacteristic _accelYChar;
    private GattCharacteristic _accelZChar;
    private GattCharacteristic _gyroXChar;
    private GattCharacteristic _gyroYChar;
    private GattCharacteristic _gyroZChar;

    public MainPage()
    {
        InitializeComponent();
    }

    private async void Connect_Click(object sender, RoutedEventArgs e)
    {
        // Get device by name
        var device = await Windows.Devices.Enumeration.DeviceInformation.FindAllAsync(Windows.Devices.Bluetooth.BluetoothLEDevice.GetDeviceSelectorFromDeviceName("Arduino Accelerometer and Gyroscope")).AsTask();
        var bleDevice = await Windows.Devices.Bluetooth.BluetoothLEDevice.FromIdAsync(device.First().Id);

        // Get service and characteristics by UUID
        _service = bleDevice.GetGattService(new Guid("1101"));
        _accelXChar = _service.GetCharacteristics(new Guid("2101")).First();
        _accelYChar = _service.GetCharacteristics(new Guid("2102")).First();
        _accelZChar = _service.GetCharacteristics(new Guid("2103")).First();
        _gyroXChar = _service.GetCharacteristics(new Guid("2104")).First();
        _gyroYChar = _service.GetCharacteristics(new Guid("2105")).First();
        _gyroZChar = _service.GetCharacteristics(new Guid("2106")).First();

        // Register for value changed event
        _accelXChar.ValueChanged += AccelXChar_ValueChanged;
        _accelYChar.ValueChanged += AccelYChar_ValueChanged;
        _accelZChar.ValueChanged += AccelZChar_ValueChanged;
        _gyroXChar.ValueChanged += GyroXChar_ValueChanged;
        _gyroYChar.ValueChanged += GyroYChar_ValueChanged;
        _gyroZChar.ValueChanged += GyroZChar_ValueChanged;

        // Enable notifications
        await _accelXChar.WriteClientCharacteristicConfigurationDescriptorAsync(GattClientCharacteristicConfigurationDescriptorValue.Notify);
        await _accelYChar.WriteClientCharacteristicConfigurationDescriptorAsync(GattClientCharacteristicConfigurationDescriptorValue.Notify);
        await _accelZChar.WriteClientCharacteristicConfigurationDescriptorAsync(GattClientCharacteristicConfigurationDescriptorValue.Notify);
        await _gyroXChar.WriteClientCharacteristicConfigurationDescriptorAsync(GattClientCharacteristicConfigurationDescriptorValue.Notify);
        await _gyroYChar.WriteClientCharacteristicConfigurationDescriptorAsync(GattClientCharacteristicConfigurationDescriptorValue.Notify);
        await _gyroZChar.WriteClientCharacteristicConfigurationDescriptorAsync(GattClientCharacteristicConfigurationDescriptorValue.Notify);

        private void AccelXChar_ValueChanged(GattCharacteristic sender, GattValueChangedEventArgs args)
        {
            // Get value from args
            var data = new byte[args.CharacteristicValue.Length];
            DataReader.FromBuffer(args.CharacteristicValue).ReadBytes(data);

            // Convert value to float
            var accelX = BitConverter.ToSingle(data, 0);

            // Update UI
            AccelXValue.Text = accelX.ToString();
        }

        private void AccelYChar_ValueChanged(GattCharacteristic sender, GattValueChangedEventArgs args)
        {
            // Get value from args
            var data = new byte[args.CharacteristicValue.Length];
            DataReader.FromBuffer(args.CharacteristicValue).ReadBytes(data);

            // Convert value to float
            var accelY = BitConverter.ToSingle(data, 0);

            // Update UI
            AccelYValue.Text = accelY.ToString();
        }

        private void AccelZChar_ValueChanged(GattCharacteristic sender, GattValueChangedEventArgs args)
        {
            // Get value from args
            var data = new byte[args.CharacteristicValue.Length];
            DataReader.FromBuffer(args.CharacteristicValue).ReadBytes(data);

            // Convert value to float
            var accelZ = BitConverter.ToSingle(data, 0);

            // Update UI
            AccelZValue.Text = accelZ.ToString();
        }

        private void GyroXChar_ValueChanged(GattCharacteristic sender, GattValueChangedEventArgs args)
        {
            // Get value from args
            var data = new byte[args.CharacteristicValue.Length];
            DataReader.FromBuffer(args.CharacteristicValue).ReadBytes(data);

            // Convert value to float
            var gyroX = BitConverter.ToSingle(data, 0);

            // Update UI
            GyroXValue.Text = gyroX.ToString();
        }

        private void GyroYChar_ValueChanged(GattCharacteristic sender, GattValueChangedEventArgs args)
        {
            // Get value from args
            var data = new byte[args.CharacteristicValue.Length];
            DataReader.FromBuffer(args.CharacteristicValue).ReadBytes(data);

            // Convert value to float
            var gyroY = BitConverter.ToSingle(data, 0);

            // Update UI
            GyroYValue.Text = gyroY.ToString();
        }

        private void GyroZChar_ValueChanged(GattCharacteristic sender, GattValueChangedEventArgs args)
        {
            // Get value from args
            var data = new byte[args.CharacteristicValue.Length];
            DataReader.FromBuffer(args.CharacteristicValue).ReadBytes(data);

            // Convert value to float
            var gyroZ = BitConverter.ToSingle(data, 0);

            // Update UI
            GyroZValue.Text = gyroZ.ToString();
        }
    }
}