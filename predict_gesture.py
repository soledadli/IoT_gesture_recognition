import numpy as np
import pandas as pd
import os, os.path
import tensorflow as tf
import time
import serial
from preprocess_data import *
import schedule
import time
from datetime import datetime, timedelta


ser = serial.Serial()
port = "/dev/cu.usbmodem14301"
baud = 115200
time_out = 30

test_dir = "data_pipeline/test_data"


# Get Data from imu sensor
def get_imu_data():
    arduino = serial.Serial(port, baud, serial.EIGHTBITS, serial.PARITY_NONE ,serial.STOPBITS_ONE, time_out)
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
    while line <= samples:
        try:
            data = str(arduino.readline(), 'utf-8')
            print(data)
            if data.startswith("t"):
                vals = data.strip().split(":")
                lst = [vals[index] for index in [1, 3, 5, 7]]

            elif data.startswith("g"):
                vals2 = data.strip().split(":")
                lst2 = lst + [vals2[index] for index in [1, 3, 5]]
                res = ",".join(lst2)

            vals = [float(i) for i in res]
            print(vals)
            print(res)
            return vals

        except:
            print("Interruption")
            break

def segement_predict_data(feature, time_steps=5, step=2):
    '''
    (row, column, depth): row * column should be the length of dataframe
    to include all the data points in the dataframe
    '''
    Xs = []
    for i in range(0, len(feature) - time_steps, step):
        v = feature.iloc[i:(i + time_steps)].values
        # print(feature.iloc[i:(i + time_steps)]) # to test the best segemented sizes
        Xs.append(v)
        print(np.shape(Xs))
    return np.array(Xs)


@tf.autograph.experimental.do_not_convert
def predict_motion(model, test_dir, motion:list):
    predict_df = pd.DataFrame(columns= ["name","time","predictions"])
    # read files should be predicted from the directory
    for path, currentDirectory, files in os.walk(test_dir):
        for f in files:
            filename = os.path.join(path,f)
            df = pd.read_csv(filename,  index_col=[0])
            #  df = pd.read_csv("data_pipeline/clean_data/" +  filename + ".csv")
            # scale the prediction file data
            dfs = scale_data(df, f)
            # preprocessing the data for model prediction
            X = segement_predict_data(
                dfs[['aX', 'aY', "aZ", "gX", "gY", "gZ"]], 5, 1)
            # predict the model
            predictions = model.predict(X)
            # identifying predicted motions
            category = np.argmax(predictions, axis=1)
            print( f, category)
            for i in category:
                # appending new predictions to the predict_file
                hour = datetime.now().strftime("%H:%M:%S")
                predict_df = predict_df.append({"name": f, "time" : hour , 'predictions':i , "motion" : motion[i]}, ignore_index=True)
    date = datetime.now().strftime("%Y-%m-%d")
    # create a new df of predictions per day
    predict_df.to_csv('predictions/' + date + "-predictions.csv", mode='a',header= False)
    return category

if __name__ == "__main__":
  #  vals = get_imu_data()
  # load Model
    model = tf.keras.models.load_model('models/lstm_model.h5')
  #  tp = pd.DataFrame()‚
    schedule.every(10).seconds.until(timedelta(seconds=20)).do(lambda: predict_motion(model, test_dir, ["test1","test2"]))

    while True:
        try:
            schedule.run_pending()
            time.sleep(5)
        except:
            schedule.clear()