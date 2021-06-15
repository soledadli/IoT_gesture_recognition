# Movuino Gesture Recognition (TinyML)
## Table of Contents
* [Troubleshooting](#trouble-shooting)


## Movuino Troubleshooting 
Q1: The Arduino IDE cannot recognize the port for Movuino
- Check whether the board is correct. The correct version is `Movuino Open Health Band v0.2.7.4`
- Check whether the connection is good. 
  - Check whether the red LED, charging indicator light, is on.
  - Check whether the board is on. If not, press the black switch for 2 seconds. 
- Double-click the reset button on the Movuino board. (Red LED light will blink when you reset the board)
- Use the Debugging Board for testing codes

Q2: Having trouble compiling codes on Movuino (There is a higher chance that when compiling codes on Movuino, Arduino IDE may crush more often when there are bugs on the code or the model size is too big.)
- Check whether you use the right version of the TensorFlowLite Library.
  - Open **Manage Libraries** -> Search for **Arduino_TensorFlowLite** -> Check the version -> The one I tested and worked is `1.14.0 - Alpha`
  - Do not choose versions with precompiled labels. They may not work.
- Verify the codes before you uploading them to Movuino
- Try uploading the imu data parts and test whether they work. If so, upload the tensorflow parts and the model part then.
- Unplug the board, replug it, and reupload the codes 

Q3: Disk get ejected when after uploading the sketch
- Open the Serial Monitor, the sketch may be already successfully uploaded.
- Double-click the reset button, and replug it back to the computer, and run the sketch. 

Q4: After uploading the sketch, there is no Serial.println information on Serial Monitor
- Parts of your code may crush. You may want to debug your code paragraphs by paragraphs 
