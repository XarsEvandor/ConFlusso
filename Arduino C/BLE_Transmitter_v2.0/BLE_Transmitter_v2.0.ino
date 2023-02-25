#include <ArduinoBLE.h>
#include <Arduino_LSM9DS1.h>

// Constants for BLE characteristics
const char* SERVICE_UUID = "1101";

const char* ACCEL_UUID = "2101";
const char* GYRO_UUID = "2102";

// Variables to store sensor data
int16_t accelX, accelY, accelZ;
int16_t gyroX, gyroY, gyroZ;

float x, y, z;
float l, m, n;

// Create BLE service and characteristics for accelerometer and gyroscope data
BLEService customService(SERVICE_UUID);

BLECharacteristic customAccelChar(ACCEL_UUID, BLERead | BLENotify, 6);
BLECharacteristic customGyroChar(GYRO_UUID, BLERead | BLENotify, 6);

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
  customService.addCharacteristic(customGyroChar);
  customService.addCharacteristic(customAccelChar);

  // Add service to BLE
  BLE.addService(customService);

  // Initialize characteristic values
  customAccelChar.writeValue("");
  customGyroChar.writeValue("");

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

      char accelData[20]; // Maximum length of the string

      // Combine accelerometer data into a single string
      sprintf(accelData, "%d,%d,%d", x, y, z);

      char gyroData[20]; // Maximum length of the string

      // Combine accelerometer data into a single string
      sprintf(gyroData, "%d,%d,%d", x, y, z);

      // Update characteristic values
      customAccelChar.writeValue(accelData);
      customGyroChar.writeValue(gyroData);

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
    accelX = (1 + floor(x)) * 100;
    accelY = (1 + floor(y)) * 100;
    accelZ = (1 + floor(z)) * 100;
  }

  if(IMU.gyroscopeAvailable()){
    IMU.readGyroscope(l, m, n);
    gyroX = (2000 + floor(l)) / 20;
    gyroY = (2000 + floor(m)) / 20;
    gyroZ = (2000 + floor(n)) / 20;
  
  }
}