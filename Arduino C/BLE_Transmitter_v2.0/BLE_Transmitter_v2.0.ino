#include <ArduinoBLE.h>
#include <Arduino_LSM9DS1.h>
// #include <mbed.h>

// mbed::Ticker counterTicker;

// Constants for BLE characteristics
const char* SERVICE_UUID = "1101";

const char* ACCEL_UUID = "2101";
const char* GYRO_UUID = "2102";

// Variables to store sensor data
int16_t accelX, accelY, accelZ;
int16_t gyroX, gyroY, gyroZ;

float x, y, z;
float l, m, n;

int nTicks = 0;
bool bIsReady = false;

uint8_t accelData[12];
uint8_t gyroData[12];

// Create BLE service and characteristics for accelerometer and gyroscope data
BLEService customService(SERVICE_UUID);

BLECharacteristic customAccelChar(ACCEL_UUID, BLERead | BLENotify, 12);
BLECharacteristic customGyroChar(GYRO_UUID, BLERead | BLENotify, 12);

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
  // customAccelChar.writeValue("");
  // customGyroChar.writeValue("");

  // Start BLE advertising
  BLE.advertise();

  // counterTicker.attach_us( ReadAndSend, 5000 ); // Call ISRcounter function every 100 us. 
}


void loop() {
  BLEDevice central = BLE.central();

  if(central){
    Serial.print("Connected to central: ");
    Serial.println(central.address());
    digitalWrite(LED_BUILTIN, HIGH);



    while (central.connected()) {
      bIsReady = true;
        read_Accel();


        // Combine accelerometer data into a single string
        // sprintf(accelData, "%3d,%3d,%3d", accelX, accelY, accelZ);
        
        accelData[0] = lowByte(accelX);
        accelData[1] = highByte(accelX);

        accelData[2] = lowByte(accelY);
        accelData[3] = highByte(accelY);
        
        accelData[4] = lowByte(accelZ);
        accelData[5] = highByte(accelZ);

        // Combine accelerometer data into a single string
        // sprintf(gyroData, "%3d,%3d,%3d", gyroX, gyroY, gyroZ);
      
        accelData[6] = lowByte(gyroX);
        accelData[7] = highByte(gyroX);

        accelData[8] = lowByte(gyroY);
        accelData[9] = highByte(gyroY);

        accelData[10] = lowByte(gyroZ);
        accelData[11] = highByte(gyroZ);   
        

      
        // Update characteristic values
        customAccelChar.writeValue(accelData, 12);
        // customGyroChar.writeValue(gyroData);

        // ReadAndSend();

      if (nTicks % 5 == 0)
      {
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
      nTicks++;
      delay(2);
    }
    bIsReady = false;
  }

  digitalWrite(LED_BUILTIN, LOW);
  Serial.print("Disconnected from central: ");
  Serial.println(central.address());

}

// void ReadAndSend()
// {
//   if (bIsReady)
//   {
//     read_Accel();


//     // Combine accelerometer data into a single string
//     sprintf(accelData, "%3d,%3d,%3d", accelX, accelY, accelZ);

//     // Combine accelerometer data into a single string
//     sprintf(gyroData, "%3d,%3d,%3d", gyroX, gyroY, gyroZ);


//     // Update characteristic values
//     customAccelChar.writeValue(accelData);
//     customGyroChar.writeValue(gyroData);
//   }
// }

void read_Accel(){
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
    accelX = (int16_t)(x * 1000);
    accelY = (int16_t)(y * 1000);
    accelZ = (int16_t)(z * 1000);

    // accelX = 0;
    // accelY = 1;
    // accelZ = -1;

    //accelX = (1 + floor(x)) * 100;
    //accelY = (1 + floor(y)) * 100;
    //accelZ = (1 + floor(z)) * 100;
  }

  if(IMU.gyroscopeAvailable()){
    IMU.readGyroscope(l, m, n);
    gyroX = (int16_t)(l * 1000);
    gyroY = (int16_t)(m * 1000);
    gyroZ = (int16_t)(n * 1000);


    // gyroX = -32768;
    // gyroY = 32767;
    // gyroZ = 255;
    //gyroX = (2000 + floor(l)) / 20;
    //gyroY = (2000 + floor(m)) / 20;
    //gyroZ = (2000 + floor(n)) / 20;
  
  }
}