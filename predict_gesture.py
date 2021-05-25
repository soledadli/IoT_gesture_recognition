import numpy as np
import pandas as pd
import datetime
import re
import os, os.path
import time
import random
import tensorflow as tf
import serial


ser = serial.Serial()
port = "/dev/cu.usbmodem14301"
baud = 115200
time_out = 30

#arduino = None
arduino = serial.Serial(port, baud, serial.EIGHTBITS, serial.PARITY_NONE ,serial.STOPBITS_ONE, time_out)

#load Model
# model = tf.keras.models.load_model('/model/saved_model.pb')


# Get Data from imu sensor

def get_imu_data():
    global arduino
    lst = []
    if not arduino:
        # open serial port
        arduino = serial.Serial(port, baud, time_out)
        # check which port was really used
        print("Opened", arduino.name)
        # Flush input
        time.sleep(3)
        arduino.readline()

    samples = 30
    line = 0
    # Take specific samples from Microcontrollers
    while line < samples:
        try:
            data = str(arduino.readline(), 'utf-8')
            line += 1
            for line in range(samples):
                if data.startswith("t"):
                    vals = data.strip().split(":")
                    lst = [vals[index] for index in [1, 3, 5, 7]]

                elif data.startswith("g"):
                    vals2 = data.strip().split(":")
                    lst2 = lst + [vals2[index] for index in [1, 3, 5]]

                vals = [float(i) for i in lst2]
            print(vals)
            print(lst2)
            return vals

        except:
            print("Interruption")
            break


