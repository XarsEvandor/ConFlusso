#include <ArduinoBLE.h>
#include <Arduino_LSM9DS1.h>
#include "MadgwickAHRS.h"

// ................. Settings .................
const bool USE_REPORTED_SENSOR_RATE = false;
float sensorRate = 232.69; // We have measured the sensor's sampling rate including BLE delays at 111Hz.

const bool ENABLE_BLE = true;
const int MIN_RSSI = -85;
const char* SERVICE_UUID = "477fcf1c-b91c-4c23-9004-95211c661945";
const char* ACCEL_UUID = "eebf853b-a580-424c-a827-d6600f4253e1";

const int QUEUE_SIZE = 64;
const int BYTES_PER_SAMPLE = 10;
const int BYTES_OF_CHARACTERISTIC = 16;

//[>] Issue with delays from BLE library: https://github.com/arduino-libraries/ArduinoBLE/issues/113
const int MAX_SAMPLES_FOR_PACKET = 3;
// Average Dt = 36msec (std: 1011 μs, max=66msec). Average Sampling Period: 9043μs.
//const int MAX_SAMPLES_FOR_PACKET = 4;
// Average Dt = 72msec (std: 653 μs, max=95msec). Average Sampling Period: 9020μs.
//const int MAX_SAMPLES_FOR_PACKET = 8;
// ...........................................


//========================================
struct TaskCycle
{
  unsigned long previousMoment = 0;
  unsigned long delta = 0;
  unsigned long period = 0;
  bool MustRun = false;
  int valueCount = 0;
};
//========================================
struct SensorSample
{
  float heading = 0;
  float pitch = 0;
  float roll = 0;
  float valueCount = 0;
};
//========================================


// Initialize a Madgwick filter:
Madgwick filter;

// Create BLE service and characteristics for accelerometer and gyroscope data
bool IsBLEConnected = false;
BLEDevice central;
BLEService customService(SERVICE_UUID);
BLECharacteristic characteristic(ACCEL_UUID, BLERead | BLENotify, BYTES_OF_CHARACTERISTIC); 

TaskCycle taskSampling;
TaskCycle taskCreatePacket;
TaskCycle taskManageConnection;
TaskCycle taskTransmitting;
TaskCycle taskPrint;

SensorSample sample;

// ============================ Circular Queue Implementation ===========================
uint8_t dataPacket[QUEUE_SIZE][BYTES_OF_CHARACTERISTIC]; 
int packetCount = 0;
int firstPacketIndex = 0;
int lastPacketIndex = -1;
// -----------------------------------------------------------------------------
bool QueueIsFull()
{
  return packetCount >= QUEUE_SIZE;
}
// -----------------------------------------------------------------------------
bool QueueIsEmpty()
{
  return (packetCount == 0);
}
// -----------------------------------------------------------------------------
bool Enqueue()
{
  boolean bCanEnqueue = !QueueIsFull();
  if (bCanEnqueue)
  {
      // We get the remainder of the division with the queue capacity. 
      // This ensures the wrap-around.
      lastPacketIndex = (lastPacketIndex + 1) % QUEUE_SIZE;
      packetCount++;
  }
  return bCanEnqueue;
}
// -----------------------------------------------------------------------------
void Dequeue()
{
  if (!QueueIsEmpty())
  {
    firstPacketIndex = (firstPacketIndex + 1) % QUEUE_SIZE;
    packetCount--;    
  }
}
// -----------------------------------------------------------------------------
// ====================================================================================





// -----------------------------------------------------------------------------
// Setups BLE characteristic
void SetupBLE()
{
  if (!ENABLE_BLE)
    return;

  // Set LED pin as output
  pinMode(LED_BUILTIN, OUTPUT);

  delay(200);
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
  customService.addCharacteristic(characteristic);

  // Add service to BLE
  BLE.addService(customService); 

  // Start BLE advertising
  BLE.advertise();      
  
}
// ---------------------------------------------------------------------------------
// Connects/Disconnect to BLE central
bool ManageConnection()
{
  if (!ENABLE_BLE)
    return false;

  bool bHasJustConnected = false;

  if (!IsBLEConnected)
  {
    central = BLE.central();
    if(central)
    {
      bHasJustConnected = true;
      delay(300);
      BLE.stopAdvertise();
      delay(300);
      IsBLEConnected = true;

      Serial.print("Connected to central: ");
      Serial.println(central.address());    

      if (central.hasLocalName()) 
        Serial.print("Local name: ");
        Serial.println(central.localName());
    }
  }
  else 
  {
    if (!central.connected())
    {
      digitalWrite(LED_BUILTIN, LOW);
      Serial.print("Disconnected from central.: ");
      Serial.println(central.address());  

      IsBLEConnected = false;
      delay(300);
      BLE.advertise();
      delay(300);      
    }
  }

  return bHasJustConnected;
}
/// ---------------------------------------------------------------------------------
void CreateDataPacket()
{
  // Implementation of average for multiple samples. 
  float avgHeading = sample.heading / sample.valueCount;
  float avgPitch = sample.pitch / sample.valueCount;
  float avgRoll = sample.roll / sample.valueCount;
  
  sample.heading = 0;
  sample.pitch = 0;
  sample.roll = 0;
  sample.valueCount = 0;


  int16_t heading = (int16_t)avgHeading;
  int16_t pitch = (int16_t)avgPitch;
  int16_t roll = (int16_t)avgRoll;
  
  if (Enqueue())
  {
    int nSampleOffset = 0;  //Support for multiple samples in packet

    dataPacket[lastPacketIndex][nSampleOffset    ] = lowByte(heading);
    dataPacket[lastPacketIndex][nSampleOffset + 1] = highByte(heading);

    dataPacket[lastPacketIndex][nSampleOffset + 2] = lowByte(pitch);
    dataPacket[lastPacketIndex][nSampleOffset + 3] = highByte(pitch);

    dataPacket[lastPacketIndex][nSampleOffset + 4] = lowByte(roll);
    dataPacket[lastPacketIndex][nSampleOffset + 5] = highByte(roll);

    //TODO: This is for compatibility with Python code, need to start at  nSampleOffset + 6
    unsigned long timestamp = micros();
    dataPacket[lastPacketIndex][nSampleOffset + 6] = timestamp & 0xFF;
    dataPacket[lastPacketIndex][nSampleOffset + 7] = (timestamp >> 8) & 0xFF;
    dataPacket[lastPacketIndex][nSampleOffset + 8] = (timestamp >> 16) & 0xFF;
    dataPacket[lastPacketIndex][nSampleOffset + 9] = (timestamp >> 24) & 0xFF;

    nSampleOffset += BYTES_PER_SAMPLE;
  }

}
/// ---------------------------------------------------------------------------------










// -----------------------------------------------------------------------------
void setup() {
  Serial.begin(9600);
  // attempt to start the IMU:
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU");
    // stop here if you can't access the IMU:
    while (true);
  }

  /*
    https://github.com/FemmeVerbeek/Arduino_LSM9DS1
    nr 	setAccelODR(nr) 	setGyroODR(nr) 	setMagnetODR(nr)
     0 	  Gyro&Accel off 	Gyro off 	        0.625 Hz
     1 	  10 Hz 	        10 Hz 	          1.25 Hz
     2 	  50 Hz 	        50 Hz 	          2.5 Hz
     3 	  119 Hz 	        119 Hz 	          5 Hz
     4 	  238 Hz 	        238 Hz 	          10 Hz
     5 	  476 Hz 	        476 Hz 	          20 Hz
  */
  IMU.setAccelODR(4);
  IMU.setGyroODR(4);

  if (USE_REPORTED_SENSOR_RATE)
    sensorRate = IMU.accelerationSampleRate();
  filter.begin(sensorRate);

  SetupBLE();

  taskSampling.period = 1000000 / sensorRate;
  taskPrint.period = taskSampling.period * 300;
  taskCreatePacket.period = taskSampling.period * MAX_SAMPLES_FOR_PACKET;
  taskManageConnection.period = taskCreatePacket.period;
  taskTransmitting.period = 200;// taskSampling.period;

  unsigned long nCurrentMoment = micros();
  taskPrint.previousMoment = nCurrentMoment;
  taskCreatePacket.previousMoment = nCurrentMoment;
  taskManageConnection.previousMoment = nCurrentMoment;
  taskTransmitting.previousMoment = nCurrentMoment;
  taskSampling.previousMoment = nCurrentMoment;
}
// -----------------------------------------------------------------------------
void loop() {
  
  unsigned long nCurrentMoment = micros();
  taskPrint.delta = nCurrentMoment - taskPrint.previousMoment;
  taskPrint.MustRun = (taskPrint.delta >= taskPrint.period);

  taskManageConnection.delta = nCurrentMoment - taskManageConnection.previousMoment;
  taskManageConnection.MustRun =  (taskManageConnection.delta >= taskManageConnection.period);


  taskCreatePacket.delta = nCurrentMoment - taskCreatePacket.previousMoment;
  taskTransmitting.delta = nCurrentMoment - taskTransmitting.previousMoment;

  // <<[Sensor Sampling Task]>>
  // Sampling period determined by the availability of IMU data
  taskSampling.MustRun = IMU.accelerationAvailable() && IMU.gyroscopeAvailable(); 
  if (taskSampling.MustRun)
  {
    taskSampling.delta = nCurrentMoment - taskSampling.previousMoment;
    taskSampling.previousMoment = nCurrentMoment;

    taskSampling.period += taskSampling.delta;    
    taskSampling.valueCount++;

    // values for acceleration and rotation:
    float xAcc, yAcc, zAcc;
    float xGyro, yGyro, zGyro;

    // values for orientation:
    float roll, pitch, heading;
    // check if the IMU is ready to read:

    // read accelerometer &and gyrometer:
    IMU.readAcceleration(xAcc, yAcc, zAcc);
    IMU.readGyroscope(xGyro, yGyro, zGyro);

    // update the filter, which computes orientation:
    filter.updateIMU(xGyro, yGyro, zGyro, xAcc, yAcc, zAcc);

    // print the heading, pitch and roll
    roll = filter.getRoll();
    pitch = filter.getPitch();
    heading = filter.getYaw();
    
    // Implementation of average for multiple samples. 
    sample.roll += roll;
    sample.pitch += pitch;
    sample.heading += heading;
    sample.valueCount++;
  }

  // <<[Data Packet Creation Task]>>
  taskCreatePacket.MustRun = (sample.valueCount >= MAX_SAMPLES_FOR_PACKET);
  if (taskCreatePacket.MustRun)
  {
    taskCreatePacket.previousMoment = nCurrentMoment;

    if (taskPrint.MustRun)
    {
      taskPrint.previousMoment = nCurrentMoment;      

      if (ENABLE_BLE & (!IsBLEConnected))
      {
        Serial.print("Waiting for connection. ");
        Serial.print("Accelerometer sample rate = ");
        Serial.print(IMU.accelerationSampleRate());
        Serial.print("Hz. ");
        Serial.print("Gyroscope sample rate = ");
        Serial.print(IMU.gyroscopeSampleRate());
        Serial.println("Hz. ");
      }
      float avgHeading = sample.heading / sample.valueCount;
      float avgPitch = sample.pitch / sample.valueCount;
      float avgRoll = sample.roll / sample.valueCount;      
      int avgSamplingPeriod = taskSampling.period / taskSampling.valueCount;
      Serial.print("Queued packets:");
      Serial.print(packetCount);
      Serial.print(" Avg Sampling Period (μS):");
      Serial.print(avgSamplingPeriod);
      Serial.print(" Heading:");
      Serial.print(avgHeading);
      Serial.print(" Pitch:");
      Serial.print(avgPitch);
      Serial.print(" Roll:");
      Serial.println(avgRoll);

      taskSampling.period = 0;
      taskSampling.valueCount = 0;
    } 
    
    CreateDataPacket(); 
  }
  
  taskTransmitting.MustRun = (packetCount > 0) & (taskTransmitting.delta >= taskTransmitting.period);
  
  // <<[Connection Management Task]>>
  if (taskManageConnection.MustRun)
  {
    taskManageConnection.previousMoment = nCurrentMoment;
    bool bHasJustConnected = ManageConnection();
    if (bHasJustConnected)
      taskTransmitting.MustRun = true;
  }
   
  // <<[Data Transmission Task]>>
  if (taskTransmitting.MustRun)
  {
    taskTransmitting.previousMoment = micros();

    //taskTransmitting.previousMoment = micros();
    if (ENABLE_BLE & IsBLEConnected)
    {
      //[>] BLE stack stop working with RSSI zero. https://forum.arduino.cc/t/writing-to-characteristic-via-ble-gets-stuck-periodically/678894
      int nRSSI = BLE.rssi();
      if ((nRSSI != 0) & (nRSSI > MIN_RSSI))
      {
        characteristic.writeValue(dataPacket[firstPacketIndex], BYTES_OF_CHARACTERISTIC);
        Dequeue();
      }
    }
    else
      Dequeue();
  }
}