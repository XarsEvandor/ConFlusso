#include <ArduinoBLE.h>
#include <Arduino_LSM9DS1.h>

// Constants for BLE characteristics
const char* SERVICE_UUID = "1101";
const char* ACCEL_X_UUID = "2101";
const char* ACCEL_Y_UUID = "2102";
const char* ACCEL_Z_UUID = "2103";
const char* GYRO_X_UUID = "2104";
const char* GYRO_Y_UUID = "2105";
const char* GYRO_Z_UUID = "2106";

// Variables to store sensor data
float accelX, accelY, accelZ;
float gyroX, gyroY, gyroZ;

float x, y, z;
float l, m, n;

// Create BLE service and characteristics for accelerometer and gyroscope data
BLEService customService(SERVICE_UUID);
BLEUnsignedIntCharacteristic customAccelXChar(ACCEL_X_UUID, BLERead | BLENotify);
BLEUnsignedIntCharacteristic customAccelYChar(ACCEL_Y_UUID, BLERead | BLENotify);
BLEUnsignedIntCharacteristic customAccelZChar(ACCEL_Z_UUID, BLERead | BLENotify);
BLEUnsignedIntCharacteristic customGyroXChar(GYRO_X_UUID, BLERead | BLENotify);
BLEUnsignedIntCharacteristic customGyroYChar(GYRO_Y_UUID, BLERead | BLENotify);
BLEUnsignedIntCharacteristic customGyroZChar(GYRO_Z_UUID, BLERead | BLENotify);

void setup() {
  // Start the IMU
  IMU.begin();

  // Start serial communication
  Serial.begin(9600);
  while (!Serial) {
    ;
  }

  // Set LED pin as output
  pinMode(LED_BUILTIN, OUTPUT);

  // Initialize BLE
  if (!BLE.begin()) {
    Serial.println("BLE failed to Initiate");
    delay(500);
    while (1) {
      ;
    }
  }

  // Set BLE device name and advertised service
  BLE.setLocalName("Arduino Accelerometer");
  BLE.setDeviceName("Arduino Accelerometer");
  BLE.setAdvertisedService(customService);

  // Add characteristics to service
  customService.addCharacteristic(customAccelXChar);
  customService.addCharacteristic(customAccelYChar);
  customService.addCharacteristic(customAccelZChar);
  customService.addCharacteristic(customGyroXChar);
  customService.addCharacteristic(customGyroYChar);
  customService.addCharacteristic(customGyroZChar);

  // Add service to BLE
  BLE.addService(customService);

  // Initialize characteristic values
  customAccelXChar.writeValue(0);
  customAccelYChar.writeValue(0);
  customAccelZChar.writeValue(0);

  customGyroXChar.writeValue(0);
  customGyroYChar.writeValue(0);
  customGyroZChar.writeValue(0);

  // Start BLE advertising
  BLE.advertise();
}

void loop() {
  BLEDevice central = BLE.central();

  if(central){
    Serial.print("Connected to central: ");
    Serial.println(central.address());
    digitalWrite(LED_BUILTIN, HIGH);

    while (central.connected()) {
      delay(200);
      read_Accel();

      // Update characteristic values
      customAccelXChar.writeValue(accelX);
      customAccelYChar.writeValue(accelY);
      customAccelZChar.writeValue(accelZ);
      customGyroXChar.writeValue(gyroX);
      customGyroYChar.writeValue(gyroY);
      customGyroZChar.writeValue(gyroZ);

      // Print sensor data to serial monitor
      Serial.print("Acceleration: X = ");
      Serial.print(accelX);
      Serial.print(" Y = ");
      Serial.print(accelY);
      Serial.print(" Z = ");
      Serial.println(accelZ);

      Serial.print("Gyroscope: X = ");
      Serial.print(gyroX);
      Serial.print(" Y = ");
      Serial.print(gyroY);
      Serial.print(" Z = ");
      Serial.println(gyroZ);
      Serial.println("");
    }
  }

  digitalWrite(LED_BUILTIN, LOW);
  Serial.print("Disconnected from central: ");
  Serial.println(central.address());

}

void read_Accel(){
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
    accelX = (1 + x) * 100;
    accelY = (1 + y) * 100;
    accelZ = (1 + z) * 100;
  }

  if(IMU.gyroscopeAvailable()){
    IMU.readGyroscope(l, m, n);
    gyroX = (2000 + l) / 20;
    gyroY = (2000 + m) / 20;
    gyroZ = (2000 + n) / 20;
  
  }
}