# Movuino Gesture Recognition (TinyML)
## Table of Contents

* [Instatllation Environments](#environment)
* [Instructions on magic wand example on Arduino Nano 33](#instruction_nano)
* [Instructions on deploying models on Movuino](#instruction_movuino)
* [Instructions on running Dashboard](#instruction_dash)
* [Flowcharts](#flowchart)
* [Movuino Troubleshooting](#trouble-shooting)


## Instatllation Environments
- Clone this repository with the following command

```
git clone https://github.com/soledadli/Movuino_gesture_recognition.git
```
Requirements includes:
```
Python == 3.8.3
Arduino == 1.8.12
Arduino_LSM9DS1 == 1.0.0
Arduino_TensorFlowLite == 1.14.0 - Alpha 

```
## Instructions on magic wand example on Arduino Nano 33
```

```
## Instructions on deploying models on Movuino
- Run the extract_imu_data.py file from the terminal
```
python3 extract_imu_data.py
```
- Upload the compiled data to Google Colab
```

```
- Open the Firmware_Peripheral_Classifier.ino
```
Replace your model.h file to the previous model.h
```
- Change your model name to g_model as the picture shows

![change_model_name](https://github.com/soledadli/Movuino_gesture_recognition/blob/main/photos/change_model_name.png?raw=true)

- Upload the Arduino sketch with the new model to Movuino
- Upload the **multiCentral_Classifier.ino** to Adafruit Feather
- Open the Serial Monitor of the Adafruit Feather in Arduino IDE
- Turn on the Movuino watch
- Here are the predictions of your motion 🎈

## Flowcharts
### Use Movuino to Collect Gesture Data
![collect_data_with_movuino](https://github.com/soledadli/Movuino_gesture_recognition/blob/main/flowcharts_raw/photo/Movuino_Collect_Data.jpg?raw=true)
### Predict Motions & Plot out Real-time Predictions
![dashboard](https://github.com/soledadli/Movuino_gesture_recognition/blob/main/flowcharts_raw/photo/Dashoboard_Gesture_Recognition.png?raw=true)

## Movuino Troubleshooting 
`Q1: The Arduino IDE cannot recognize the port for Movuino`
- Check whether the board is correct. The correct version is `Movuino Open Health Band v0.2.7.4`
- Check whether the connection is good. 
  - Check whether the red LED, charging indicator light, is on.
  - Check whether the board is on. If not, press the black switch for 2 seconds. 
- Double-click the reset button on the Movuino board. (Red LED light will blink when you reset the board)
- Use the Debugging Board for testing codes

`Q2: Having trouble compiling codes on Movuino (There is a higher chance that when compiling codes on Movuino, Arduino IDE may crush more often when there are bugs on the code or the model size is too big.)`
- Check whether you use the right version of the TensorFlowLite Library.
  - Open **Manage Libraries** -> Search for **Arduino_TensorFlowLite** -> Check the version -> The one I tested and worked is `1.14.0 - Alpha`
  - Do not choose versions with precompiled labels. They may not work.
- Verify the codes before you uploading them to Movuino
- Try uploading the imu data parts and test whether they work. If so, upload the tensorflow parts and the model part then.
- Unplug the board, replug it, and reupload the codes 
- Bootloading your Movuino Board to clear out memories 
  -  Opening the Arduino IDE
  -  For board, choose `Adafruit Feather nRF52840 Feather`
  -  The bootloader option will be `0.3.3 SoftDevice s140 6.1.1`
  -  For programmer, choose `Bootloader DFU for Bluefruit nRF52`
  -  Click `Burn Bootloader`
  -  Wait the bootloading time, and reupdate your sketch after the process is finished.

`Q3: Disk get ejected when after uploading the sketch`
- Open the Serial Monitor, the sketch may be already successfully uploaded.
- Double-click the reset button, and replug it back to the computer, and run the sketch. 

`Q4: After uploading the sketch, there is no Serial.println information on Serial Monitor`
- Parts of your code may crush. You may want to debug your code paragraphs by paragraphs 
- If the Serial Monitor is still blank after after codes paragraphs by paragraphs.
  - Reset the board by double-clicking the button, until you see a message that similar to "board is ejected"
  - Unplug it and replug it
  - Test your board with a simple `Serial.println("Test")` not upload any codes related with model from `void setup()` and TensorFlow Lite Pipeline from `void loop()`  
  - If the serial monitor prints out the information `Test`, then upload the codes with TensorFlow Lite and the model 

`Q5: The Arduio IDE gets stuck or it takes a while to load the information.`
- Unplug your Movuino and replug it.
- Upload your sketch again. If your Arduino IDE still gets stuck, test your board with a simple `Serial.println("Test")` not upload any codes related with model from `void setup()` and TensorFlow Lite Pipeline from `void loop()`  
  - If the serial monitor prints out the information `Test`, then upload the codes with TensorFlow Lite and the model 


