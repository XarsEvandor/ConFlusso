#include <Arduino_LSM9DS1.h>

// sensor's sample rate is fixed at 104 Hz:
const float sensorRate = 119.00;

void setup() {
  Serial.begin(9600);
  // attempt to start the IMU:
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU");
    // stop here if you can't access the IMU:
    while (true);
  }

  // Print the CSV header
  Serial.println("Timestamp,AccX,AccY,AccZ,GyroX,GyroY,GyroZ");
}

void loop() {
  // values for acceleration and rotation:
  float xAcc, yAcc, zAcc;
  float xGyro, yGyro, zGyro;

  // check if the IMU is ready to read:
  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
    // read accelerometer & gyrometer:
    IMU.readAcceleration(xAcc, yAcc, zAcc);
    IMU.readGyroscope(xGyro, yGyro, zGyro);

    // print the timestamp and sensor values in CSV format:
    Serial.print(millis());
    Serial.print(",");
    Serial.print(xAcc);
    Serial.print(",");
    Serial.print(yAcc);
    Serial.print(",");
    Serial.print(zAcc);
    Serial.print(",");
    Serial.print(xGyro);
    Serial.print(",");
    Serial.print(yGyro);
    Serial.print(",");
    Serial.println(zGyro);
  }
}
