## Arduino Nano 33 BLE
* [Beforehanded Information](#beforehanded_information)
* [Arduino Nano 33 BLE Troubleshooting](#trouble-shooting)
* [Concepts Explanation](#concept_explanation)


## Beforehanded Information
1. The sketch may take a while to be uploaded successfully.
2. It is normal that Arduino Nano may get heated up during predictions.
3. The yellow LED light blinks because the Arduino is making predictions.
4. There are delays for the predictions in Serial Monitor.
5. Questions can be found on TroubleShooting. 


## Arduino Nano 33 BLE Troubleshooting
`Q1: The Arduino IDE `

`Q2: There are nothing predicted or shown on Serial Monitor`
- Check your TensorFlow Lite Version.
  - If you have installed `Arduino_TensorFlowLite library 2.1.0-ALPHA` on your Arduino IDE, the serial monitor will be blank until you perform gestures correctly. 
  - You can use`Arduino_TensorFlowLite == 1.14.0 - Alpha` instead, which will print out `Magic Starts` on Serial Monitor. 
- Check the way you hold Arduino. The model is trained with specific and orientation. If you hold it in a wrong way, it may not predict motions. Correct way is shown as the picture shows:![WechatIMG590](https://user-images.githubusercontent.com/67457005/122404301-62c7f580-cf7f-11eb-988b-ae4978264bea.jpeg)
  - Try with `W` and `slope` gestures first. These two are the easiest one to predict. `Ring` is a little bit harder than the first two gestures. 
  - For the `ring`, swing the Arduino Nano clockwise. Try to make the movement as smooth and stable as possible. 
   - Try to finish your movement in **1 second**
  - When doing the `slope` motion, try to make a big slope. Sometimes a small slope may not provide enough data for the model to predict the motion.  
- Uncomment the following code on  `gesture_predictor.cpp` & Reupload the Sketch & Change kConsecutiveInferenceThresholds
  - ```c++
    if (last_predict == this_predict) {
      continuous_count += 1;
      Serial.println("count" + String(continuous_count)); // uncomment this line so you can print the continuous count out 
    } else {
      continuous_count = 0;
    }```
- Now you can see how many times this motion is being predicted.
    - After seeing the counts, you can adjust the way you move, like `exaggerating your motion or finishing it faster`, to acheive a better prediction. 
    - The countinous count must be equal or larger than the `kConsecutiveInferenceThresholds` (See the explanation in Concepts part) to finalize its predictions.
    - If your `continuous_count` is always smaller than required thresholds from `kConsecutiveInferenceThresholds`, you can go to `arduino_constants.cpp` and 
    lower down the numbers.
    ```c++
    The original setup is: const int kConsecutiveInferencessholds[3] = {8, 5, 4}; 
    // 8 is for W; 5 is for Ring; 4 is for Slope.
    // You can test with the {8, 5, 4} numbers untill the predictions fit with your Arduino. 
    ```

## Concepts Explanation 
1. `kConsecutiveInferenceThresholds`:<br />
the consecutive inferences that a motion at least needs to achieve to print out the predictions (from arduino_constants.cpp)

```
e.g In the Magic Wand demo sketch, "kConsecutiveInferenceThresholds[3] = {8, 5, 4}" means that when the consecutive 
prediction for "Wing" achieves 8, the serial monitor will print "W". 

The Threshold numbers (8, 5, 4) can be tuned according to different microcontrollers, like adding or subtracting numbers. 

The predicition is made by TinyML model embedded on microcontrollers while the counts threshold is regulated manually 
after testing with microcontrollers. 
```
![kConsecutiveInferenceThresholds_explanation](https://github.com/soledadli/Movuino_gesture_recognition/blob/main/photos/kConsecutiveInferenceThresholds_explanation.png?raw=true)

