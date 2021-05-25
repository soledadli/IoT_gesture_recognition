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
port = "/dev/cu.usbmodem14101"
baud = 115200
time_out = 30

#arduino = None
arduino = serial.Serial(port, baud, time_out)

#load Model
model = tf.keras.models.load_model('/model/saved_model.pb')


# Get Data from imu sensor

def get_imu_data():
    '''
    if not arduino:
        # open serial port
        arduino = serial.Serial(port, baud, time_out)
        # check which port was really used
        print("Opened", arduino.name)
        # Flush input
        time.sleep(3)
        arduino.readline()
        '''
    data = str(arduino.readline(), 'utf-8')
    print(data)
    return data
'''
    # Poll the serial port
    line = str(serialport.readline(), 'utf-8')
    if not line:
        return None

    vals = line.replace("Uni:", "").strip().split(',')

    if len(vals) != 7:
        return None
    try:
        vals = [float(i) for i in vals]
    except ValueError:
        return ValueError

    return vals
'''