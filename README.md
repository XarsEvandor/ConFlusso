# ConFlusso
 A novel system of musical co-creation between humans and deep neural networks, using wearable devices to achieve a movement-to-note type of interfacing. 

## Arduino:
* <details><summary>BLE_Transmitter_v1.1</summary>
    <p> 
    # Arduino Accelerometer using BLE

    This code demonstrates BLE communication between an Arduino board and a central device (e.g. smartphone) using an IMU (Inertial Measurement Unit).

    ## Required Libraries
    - ArduinoBLE.h for BLE communication
    - Arduino_LSM9DS1.h for IMU communication

    ## Constants
    Define BLE characteristic UUIDs for accelerometer and gyroscope data:
    - SERVICE_UUID: BLE service UUID
    - ACCEL_X_UUID, ACCEL_Y_UUID, ACCEL_Z_UUID: BLE characteristic UUIDs for accelerometer data
    - GYRO_X_UUID, GYRO_Y_UUID, GYRO_Z_UUID: BLE characteristic UUIDs for gyroscope data

    ## Variables
    - accelX, accelY, accelZ: variables to store accelerometer data
    - gyroX, gyroY, gyroZ: variables to store gyroscope data

    ## BLE Service and Characteristics
    - Create BLE service and characteristics for accelerometer and gyroscope data
    - Add the service and characteristics to BLE
    - Advertise the BLE service

    ## `setup()` function
    - Initialize IMU and serial communication
    - Initialize BLE, set device name, and advertise service

    ## `loop()` function
    - Get the central device connection status using `BLE.central()`
    - If a central device is connected:
    - Print the central device address with `Serial.println()`
    - Turn on the LED with `digitalWrite()`
    - While the central device is connected:
        - Delay for 200ms using `delay()`
        - Read accelerometer and gyroscope data using `IMU.readAcceleration()` and `IMU.readGyro()`
        - Store the data in `accelX`, `accelY`, `accelZ`, `gyroX`, `gyroY`, `gyroZ` variables
        - Update the values of BLE characteristics with `customAccelXChar.setValue()`, `customAccelYChar.setValue()`,
        `customAccelZChar.setValue()`, `customGyroXChar.setValue()`, `customGyroYChar.setValue()`,
        `customGyroZChar.setValue()`
    - If no central device is connected:
    - Turn off the LED with `digitalWrite()`
    - Re-advertise the BLE service with `BLE.advertise()`

    ## `readAcceleration()` function
    - Read accelerometer data using `IMU.readAccel()` and store in `accelX`, `accelY`, and `accelZ`
    - Read gyroscope data using `IMU.readGyro()` and store in `gyroX`, `gyroY`, and `gyroZ`
    - Update the characteristic values using `customAccelXChar.setValue()`, `customAccelYChar.setValue()`, `customAccelZChar.setValue()`, `customGyroXChar.setValue()`, `customGyroYChar.setValue()`, `customGyroZChar.setValue()`
    - Notify the central device of the updated values using `customAccelXChar.notify()`, `customAccelYChar.notify()`, `customAccelZChar.notify()`, `customGyroXChar.notify()`, `customGyroYChar.notify()`, `customGyroZChar.notify()`

    </p>

## C#:
* <details><summary>UWP Hello (Abandoned)</summary>
    <p>
        Class SensorAttribute:
  This class is used to receive data from a BLE (Bluetooth Low Energy) sensor and store the readings.
  It has two instance variables, `__service` and `__characteristic`, and a list `__values` to store the readings.
  It also has two properties, `Values` and `__isReadingValues` for accessing and modifying the readings.
  
  Attributes:
    - __service (GattDeviceService): An object representing a GATT (Generic Attribute Profile) device service.
    - __characteristic (GattCharacteristic): An object representing a characteristic of a BLE service.
    - __values (List[float]): A list to store the readings from the sensor.
    - __isReadingValues (bool): A boolean flag to check if the values are being read.
    - __serviceGUID (String): A string representing the UUID (Universally Unique Identifier) of the service.
    - __characteristicGUID (String): A string representing the UUID of the characteristic.
    
  Properties:
    - Values (List[float]): Returns a list of the stored readings.
    
  Methods:
    - __init__(self, p_sServiceGUID, p_sCharacteristicGUID): Initializes the `__serviceGUID` and `__characteristicGUID` instance variables.
    - Initialize(self): Initializes the connection to the BLE sensor, gets the `__service` and `__characteristic` objects, sets up a listener for characteristic value changes, and starts receiving notifications from the sensor.
    - ValueChanged(self, sender, args): A callback method that gets called when the characteristic value changes. It reads the value from the `args` and converts it to a float, then stores the value in the `__values` list.

    </p>

* <details><summary>BLE_DotNet</summary>
    <p>
    
    # BLE_DotNet 

    ## Dependencies
    - .NET framework
    - Windows Bluetooth API

    ## Attributes

    ### `private string _deviceName`
    Stores the name of the device.

    ### `private Guid _serviceUuid`
    Stores the unique identifier for the service offered by the device.

    ## Properties

    ### `DeviceName`
    Gets or sets the name of the device.

    ### `ServiceUuid`
    Gets or sets the unique identifier for the service offered by the device.

    ## Methods

    ### `Connect()`
    Establishes a connection to the device.

    ### `Disconnect()`
    Terminates the connection to the device.

    ### `WriteData(byte[] data)`
    Writes data to the device.

    ### `ReadData()`
    Reads data from the device.

    ## Summary
    The BLE_DotNet class allows for communication with a Bluetooth Low Energy (BLE) device using the .NET framework and Windows Bluetooth API. It provides methods for connecting to, disconnecting from, writing data to, and reading data from a BLE device. The device name and unique service identifier are stored as properties and can be accessed and modified.
    </p>