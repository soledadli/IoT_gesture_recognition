/* Copyright 2019 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#include "accelerometer_handler.h"
#include "constants.h"
#include <SPI.h>
#include <Wire.h> 

#include <Arduino.h>
#include <MPU9250_asukiaaa.h>
#define MPU9250_ADDRESS 0x69  // Device address when ADO = 1
#define INT_STATUS       0x3A
#define INT_PIN_CFG      0x37
#define INT_ENABLE       0x38
#define WHO_AM_I_MPU9250 0x75 // Should return 0x71
byte c = readByte(MPU9250_ADDRESS, WHO_AM_I_MPU9250);  // Read WHO_AM_I register for MPU-9250



MPU9250_asukiaaa mySensor(0x69);
float aX, aY, aZ, aX3, aSqrt, gX, gY, gZ, mDirection, mX, mY, mZ,mX2,mY2,mZ2;
float aX2,aY2,aZ2;
float accelRange=16.0;
float gyroRange=2000.0;
uint8_t* accelBuf;
bool dataReady = false;
#define debugAcc1;




int dataMode=0; //0 : raw int | 1 : Float 
uint8_t bufAcc[10];

bool errorIMU = false;
bool errorPPG = false;
bool errorTemp = false; 
bool errorTens = false;
bool errorAcc = false;
uint8_t bufError[4];


// A buffer holding the last 200 sets of 3-channel values
float save_data[600] = {0.0};
// Most recent position in the save_data buffer
int begin_index = 0;
// True if there is not yet enough data to run inference
bool pending_initial_data = true;
// How often we should save a measurement during downsampling
int sample_every_n;
// The number of measurements since we last saved one
int sample_skip_counter = 1;


void writeByte(uint8_t address, uint8_t subAddress, uint8_t data)
{
  Wire.beginTransmission(address);  // Initialize the Tx buffer
  Wire.write(subAddress);           // Put slave register address in Tx buffer
  Wire.write(data);                 // Put data in Tx buffer
  Wire.endTransmission();           // Send the Tx buffer
}

        uint8_t readByte(uint8_t address, uint8_t subAddress)
{
  uint8_t data; // `data` will store the register data   
  Wire.beginTransmission(address);         // Initialize the Tx buffer
  Wire.write(subAddress);                  // Put slave register address in Tx buffer
  Wire.endTransmission(false);             // Send the Tx buffer, but send a restart to keep connection alive
  Wire.requestFrom(address, (uint8_t) 1);  // Read one byte from slave register address 
  data = Wire.read();                      // Fill Rx buffer with result
  return data;                             // Return data read from slave register
}



void initMPU9250()
{  

  // Set interrupt pin active high, push-pull, hold interrupt pin level HIGH until interrupt cleared,
  // clear on read of INT_STATUS, and enable I2C_BYPASS_EN so additional chips 
  // can join the I2C bus and all can be controlled by the Arduino as master
   writeByte(MPU9250_ADDRESS, INT_PIN_CFG, 0x22);    
   writeByte(MPU9250_ADDRESS, INT_ENABLE, 0x01);  // Enable data ready (bit 0) interrupt
   delay(100);
}


void configureIMU() {

  uint8_t sensorId;

  if (mySensor.readId(&sensorId) == 0) {
    Serial.println("sensorId: " + String(sensorId));
  }
  else {
    Serial.println("Error cannot read sensor ID");
    errorIMU = true;
  }

  if (!errorIMU) {
    mySensor.beginAccel();
  }
}

void updateAcc() {
  if (mySensor.accelUpdate() == 0) {

    //read sensor
    accelBuf = mySensor.accelBuff;
    //read timestamp
    uint32_t timestamp = millis();
    bufAcc[3] = (uint8_t)timestamp;
    bufAcc[2] = (uint8_t)(timestamp >>= 8);
    bufAcc[1] = (uint8_t)(timestamp >>= 8);
    bufAcc[0] = (uint8_t)(timestamp >>= 8);
    bufAcc[4] = 16;
    for (int i = 5; i <= 10; i++) {
      bufAcc[i] = accelBuf[i - 5];
      #ifdef debugAcc2
      /*
      Serial.print(String(i));
      Serial.print(":");
      Serial.print(String(bufAcc[i]));
      Serial.print(" ");
      */
      #endif
    }
    #ifdef debugAcc1
    Serial.println(" ");
    
    int16_t v = ((int16_t) accelBuf[0]) << 8 | accelBuf[1];
    aX2=((float) -v) * accelRange / (float) 0x8000; // (float) 0x8000 == 32768.0
    v = ((int16_t) accelBuf[2]) << 8 | accelBuf[3];
    aY2=((float) -v) * accelRange / (float) 0x8000; // (float) 0x8000 == 32768.0
    v = ((int16_t) accelBuf[4]) << 8 | accelBuf[5];
    aZ2=((float) -v) * accelRange / (float) 0x8000; // (float) 0x8000 == 32768.0
   /*
    Serial.print(String(aX2));
    Serial.print(" ");   
    Serial.print(String(aY2));   
    Serial.print(" ");   
    Serial.print(String(aZ2));   
    Serial.println(" ");  
    */      
    #endif
    dataReady = true;
  } else {
    Serial.println("Cannot read accel values");
  }
}


TfLiteStatus SetupAccelerometer(tflite::ErrorReporter* error_reporter) {
  // Wait until we know the serial port is ready
  configureIMU();
  while (!Serial) {
  }
 /*
  //Switch on the IMU;
  if (!beginAccel) {
    error_reporter->Report("Failed to initialize IMU");
    return kTfLiteError;
  }
*/
  // Determine how many measurements to keep in order to
  // meet kTargetHz
  float sample_rate = 119; // 119 from Arduino Nano 33
  sample_every_n = static_cast<int>(roundf(sample_rate / kTargetHz)); // 5 from Arduino Nano 33

  error_reporter->Report("Magic starts!");

  return kTfLiteOk;
}

bool ReadAccelerometer(tflite::ErrorReporter* error_reporter, float* input,
                       int length, bool reset_buffer) {
  // Clear the buffer if required, e.g. after a successful prediction
  if (reset_buffer) {
    memset(save_data, 0, 600 * sizeof(float));
    begin_index = 0;
    pending_initial_data = true;
  }
 
  // Keep track of whether we stored any new data
  bool new_data = false;
 // updateAcc();
  // Loop through new samples and add to buffer

    // aX3 = 0.08;
  //while(aSum >= 1.2) {
  // while (fabs(mySensor.accelX()) >= 0.04) {
    // Throw away this sample unless it's the nth
    initMPU9250();

    if (readByte(MPU9250_ADDRESS, INT_STATUS) & 0x01) {
      Serial.println("readbyte     " + String(readByte(MPU9250_ADDRESS, INT_STATUS) & 0x01));
 
    
   // while(aX3 >= 0.05) {
    updateAcc();
      
    if (sample_skip_counter != sample_every_n) {
      sample_skip_counter += 1; // 2, 3, 4, 5
   //   continue;
    }
  
    // Write samples to our buffer, converting to milli-Gs
    // and flipping y and x order for compatibility with
    // model (sensor orientation is different on Arduino
    // Nano BLE Sense compared with SparkFun Edge)
     
  // Serial.println("ax           "+ String(mySensor.accelX()));

    save_data[begin_index++] = aX2 * 1000;
    save_data[begin_index++] = aY2 * 1000;
    save_data[begin_index++] = aZ2 * 1000;


    // Since we took a sample, reset the skip counter
    sample_skip_counter = 1;
    // If we reached the end of the circle buffer, reset
    if (begin_index >= 600) {
      begin_index = 0;
    }
    new_data = true;  
    aX3 = mySensor.accelX();
    Serial.println("Inside while");
  }
  Serial.println("outside while");
  // Skip this round if data is not ready yet
  if (!new_data) {
    return false;
  }
  

  // Check if we are ready for prediction or still pending more initial data
  if (pending_initial_data && begin_index >= 200) {
    pending_initial_data = false;
  }

  // Return if we don't have enough data
  if (pending_initial_data) {
    return false;
  }

 
  // Copy the requested number of bytes to the provided input tensor
  for (int i = 0; i < length; ++i) {
    int ring_array_index = begin_index + i - length;
    if (ring_array_index < 0) {
      ring_array_index += 600;
    }
    input[i] = save_data[ring_array_index];
  //  Serial.println("i    " + String(i) + "input      " + String(input[i]));
   

  }
  return true;

}
