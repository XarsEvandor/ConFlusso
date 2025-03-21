#include <ArduinoBLE.h>
#include <Arduino_LSM9DS1.h> 

// Constants for BLE characteristics
const char* SERVICE_UUID = "477fcf1c-b91c-4c23-9004-95211c661945";

const char* ACCEL_UUID = "eebf853b-a580-424c-a827-d6600f4253e1";

// Variables to store sensor data
int16_t accelX, accelY, accelZ;
int16_t gyroX, gyroY, gyroZ;

float x, y, z;
float l, m, n;

int nTicks = 0;
bool bIsReady = false;
bool bIsDebug = false;

uint8_t accelData[16]; 

// Create BLE service and characteristics for accelerometer and gyroscope data
BLEService customService(SERVICE_UUID);

BLECharacteristic customAccelArr(ACCEL_UUID, BLERead | BLENotify, 16); 

void setup() {
  // Start the IMU
  IMU.begin();

  // Start serial communication
  Serial.begin(9600);

  // Set LED pin as output
  pinMode(LED_BUILTIN, OUTPUT);

  // Attempt to initialize BLE with a maximum of 5 retries
  int maxRetries = 5;
  int currentRetry = 0;

  while (!BLE.begin() && currentRetry < maxRetries) {
      // Print error message to Serial Monitor
      Serial.println("BLE failed to Initiate. Retrying...");

      // Blink the built-in LED in a distinctive pattern to indicate failure
      for (int i = 0; i < 3; i++) { // Blink 3 times
          digitalWrite(LED_BUILTIN, HIGH); // Turn on the LED
          delay(200);                      // Wait for 200ms
          digitalWrite(LED_BUILTIN, LOW);  // Turn off the LED
          delay(200);                      // Wait for 200ms
      }

      delay(1000); // Wait for 1 second before retrying
      currentRetry++;
  }

  // If BLE still fails to initialize after retries, blink continuously
  if (currentRetry == maxRetries) {
      Serial.println("BLE failed to Initiate after multiple retries.");
      while (1) {
          digitalWrite(LED_BUILTIN, HIGH); // Turn on the LED
          delay(500);                      // Wait for 500ms
          digitalWrite(LED_BUILTIN, LOW);  // Turn off the LED
          delay(500);                      // Wait for 500ms
      }
}


  // Set BLE device name and advertised service
  BLE.setLocalName("Arduino Accelerometer");
  BLE.setDeviceName("Arduino Accelerometer");
  BLE.setAdvertisedService(customService);

  // Add characteristics to service 
  customService.addCharacteristic(customAccelArr);

  // Add service to BLE
  BLE.addService(customService); 

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
      bIsReady = true;
        read_Accel();  
        
        accelData[0] = lowByte(accelX);
        accelData[1] = highByte(accelX);

        accelData[2] = lowByte(accelY);
        accelData[3] = highByte(accelY);
        
        accelData[4] = lowByte(accelZ);
        accelData[5] = highByte(accelZ);
   
        accelData[6] = lowByte(gyroX);
        accelData[7] = highByte(gyroX);

        accelData[8] = lowByte(gyroY);
        accelData[9] = highByte(gyroY);

        accelData[10] = lowByte(gyroZ);
        accelData[11] = highByte(gyroZ);   

        unsigned long timestamp = millis();
        accelData[12] = timestamp & 0xFF;
        accelData[13] = (timestamp >> 8) & 0xFF;
        accelData[14] = (timestamp >> 16) & 0xFF;
        accelData[15] = (timestamp >> 24) & 0xFF;

         
        // Update characteristic values
        customAccelArr.writeValue(accelData, 16);  

      if ((nTicks % 1 == 0) && (bIsDebug))
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
  Serial.print("Disconnected from central.: ");
  Serial.println(central.address());

}


// Dummy data for transmittion time estimation
void read_Accel_(){
  
    accelX = (int16_t)(1 * 1000);
    accelY = (int16_t)(1 * 1000);
    accelZ = (int16_t)(1 * 1000);

    gyroX = (int16_t)(1);
    gyroY = (int16_t)(1);
    gyroZ = (int16_t)(1);      
}

void read_Accel(){
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
    accelX = (int16_t)(x * 1000);
    accelY = (int16_t)(y * 1000);
    accelZ = (int16_t)(z * 1000);
  }

  if(IMU.gyroscopeAvailable()){
    IMU.readGyroscope(l, m, n);
    gyroX = (int16_t)(l);
    gyroY = (int16_t)(m);
    gyroZ = (int16_t)(n);
  
  }
}