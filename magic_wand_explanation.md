## Concepts Explanation 
1. `kConsecutiveInferenceThresholds`:<br />
the consecutive inferences that a motion at least needs to achieve to print out the predictions (from arduino_constants.cpp)

```
e.g In the Magic Wand demo sketch, "kConsecutiveInferenceThresholds[3] = {8, 5, 4}" means that when the consecutive 
prediction for "Wing" achieves 8, the serial monitor will print "W". 

The Threshold numbers (8, 5, 4) can be tuned according to different microcontrollers, like adding or subtracting numbers. 

** The predicition is made by TinyML model embedded on microcontrollers while The counts threshold is regulated manually 
after testing with microcontrollers. 
```
![kConsecutiveInferenceThresholds_explanation](https://github.com/soledadli/Movuino_gesture_recognition/blob/main/photos/kConsecutiveInferenceThresholds_explanation.png?raw=true)
