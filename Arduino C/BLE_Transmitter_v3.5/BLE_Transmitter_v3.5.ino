#include <Arduino_LSM9DS1.h>
#include <MadgwickAHRS.h>

Madgwick filter;

// Calibration offsets
float axOffset = 0, ayOffset = 0, azOffset = 0;
float gxOffset = 0, gyOffset = 0, gzOffset = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  // Use actual sampling rate of the IMU
  float samplingRate = IMU.accelerationSampleRate();
  filter.begin(samplingRate);

  // Check if calibration is needed
  if (axOffset == 0 && ayOffset == 0 && azOffset == 0 &&
      gxOffset == 0 && gyOffset == 0 && gzOffset == 0) {
    calibrateSensors();
  } else {
    Serial.println("Using hardcoded calibration offsets.");
  }

  Serial.print("Sampling rate: ");
  Serial.print(samplingRate);
  Serial.println(" Hz");
}

void loop() {
  float ax, ay, az;
  float gx, gy, gz;

  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
    IMU.readAcceleration(ax, ay, az);
    IMU.readGyroscope(gx, gy, gz);

    // Apply calibration offsets
    ax -= axOffset;
    ay -= ayOffset;
    az -= azOffset;
    gx -= gxOffset;
    gy -= gyOffset;
    gz -= gzOffset;

    // Convert gyroscope to rad/s
    gx *= DEG_TO_RAD;
    gy *= DEG_TO_RAD;
    gz *= DEG_TO_RAD;

    filter.updateIMU(gx, gy, gz, ax, ay, az);

    Serial.print("Orientation: Yaw=");
    Serial.print(filter.getYaw());
    Serial.print(" Pitch=");
    Serial.print(filter.getPitch());
    Serial.print(" Roll=");
    Serial.println(filter.getRoll());
  }

  delay(10); // Adjust delay to match the sampling rate
}

void calibrateSensors() {
  float ax = 0, ay = 0, az = 0;
  float gx = 0, gy = 0, gz = 0;

  const int numReadings = 100;
  Serial.println("Calibrating sensors, please keep the device still...");

  for (int i = 0; i < numReadings; i++) {
    if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
      float tax, tay, taz;
      float tgx, tgy, tgz;

      IMU.readAcceleration(tax, tay, taz);
      IMU.readGyroscope(tgx, tgy, tgz);

      ax += tax; ay += tay; az += taz;
      gx += tgx; gy += tgy; gz += tgz;
      delay(10);
    }
  }

  axOffset = ax / numReadings;
  ayOffset = ay / numReadings;
  azOffset = az / numReadings;
  gxOffset = gx / numReadings;
  gyOffset = gy / numReadings;
  gzOffset = gz / numReadings;

  Serial.println("Calibration complete. Please hardcode these offsets:");
  Serial.print("Accel offsets: ");
  Serial.print(axOffset); Serial.print(" ");
  Serial.print(ayOffset); Serial.print(" ");
  Serial.print(azOffset); Serial.print(" Gyro offsets: ");
  Serial.print(gxOffset); Serial.print(" ");
  Serial.print(gyOffset); Serial.print(" ");
  Serial.println(gzOffset);
}
