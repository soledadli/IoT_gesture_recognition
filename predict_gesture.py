import numpy as np
import pandas as pd
import os, os.path
import tensorflow as tf
import time
import serial
from preprocess_data import *
from extract_imu_data import *
import schedule
import time
from datetime import datetime, timedelta
import glob


ser = serial.Serial()
port = "/dev/cu.usbmodem14301"
baud = 115200
time_out = 30

test_dir = "data_pipeline/test_data"

'''
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
'''

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
    return np.array(Xs)

def take_imu_data():
    # Name the csv file
    # Take specific samples from Microcontrollers
    hour = datetime.now().strftime("%H:%M:%S.%f")
    fullname = hour + '.csv'
    # Put the file in one specific directory
    completeName = os.path.join(main_dir, fullname)
    samples = 100
    line = 0
    for line in range(samples):
        with open(completeName, 'a') as f:
            data = str(arduino.readline(), 'utf-8')
            f.write(data)
            f.close()
    return fullname, completeName

def organize_imu_data():
    file_name, completeName = take_imu_data()
    df = pd.read_csv(completeName)
    df = clean_imudata(df)
    cleanName = os.path.join(clean_dir, file_name)
    df.to_csv(cleanName)
    return df

@tf.autograph.experimental.do_not_convert
def predict_motion(model, test_dir, motion:list):
    predict_df = pd.DataFrame(columns= ["name","time","hour","predictions"])
    # read the latest imu data file to predict the model
    list_of_files = glob.glob(test_dir+'/*.csv')
    latest_file = max(list_of_files, key=os.path.getctime)
    latest_file_name = latest_file.split("/")[2]
    latest_file_time = latest_file_name.split('.csv')[0]
    latest_file_hour = latest_file_time.split(":")[0]
    df = pd.read_csv(latest_file, index_col=[0])
    dfs = scale_data(df, "test")
    # preprocessing the data for model prediction
    X = segement_predict_data(
        dfs[['aX', 'aY', "aZ", "gX", "gY", "gZ"]], 5, 1)
    # predict the model
    predictions = model.predict(X)
    # identifying predicted motions
    category = np.argmax(predictions, axis=1)
    for i in category:
        # appending new predictions to the predict_file
        predict_df = predict_df.append({"name": latest_file_name, "time" : latest_file_time, "hour": latest_file_hour,
                                        'predictions': i, "motion" : motion[i]}, ignore_index=True)
    date = datetime.now().strftime("%Y-%m-%d")
    prediction_file_name = 'predictions/' + date + "-predictions.csv"
    # Check the latest prediction data file
    prediction_files = glob.glob('predictions/*.csv')
    latest_prediction = max(prediction_files, key=os.path.getctime)
    if latest_prediction == prediction_file_name:
        # create a new df of predictions per day
        predict_df.to_csv(prediction_file_name, mode='a',header= False)
    else:
        predict_df.to_csv(prediction_file_name, mode='a')
    return category

if __name__ == "__main__":
  # load Model
    model = tf.keras.models.load_model('models/lstm_model.h5')
    schedule.every(1).minute.do(lambda: predict_motion(model, test_dir, ["test1","test2"]))
    while True:
        organize_imu_data()
        schedule.run_pending()


