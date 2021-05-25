import serial
import os.path
import time
import pandas as pd

ser = serial.Serial()
# use search_port_name.py to get right names for the usb port
port = "/dev/cu.usbmodem14301"
baud = 115200
time_out = 2
byte=8

# Added the bytesize & parity parameter for receiving model predictions data
arduino = serial.Serial(port, baud, serial.EIGHTBITS, serial.PARITY_NONE ,time_out)
main_dir = 'test_data/'
clean_dir = 'clean_test_data/'

# Data Logging from the Serial Monitor of the Central
def log_imu_data( ):
    # Name the csv file
    name = str(input("What is the name of the file: "))
    fullname = name + '.csv'
    # Put the file in one specific directory
    completeName = os.path.join(main_dir, fullname)
    # 44 is like one minute sample
    samples = 44
    line = 0
    # Take specific samples from Microcontrollers
    while line < samples:
        try:
            with open(completeName, 'a') as f:
                data = str(arduino.readline(), 'utf-8')
                f.write(data)
                line += 1
                f.close()
        except:
            print("Interruption")
            break

    return fullname, completeName

# Clean the data
def clean_gyrodata(df):
  # Store info about columns
  col = sorted(df)[0]
  # Take Gyro data out into seperate cleaning as the format is different with Accel data
  gyro = df[df[col].apply(lambda x: x.startswith('g'))].reset_index(drop=True)
  # Split data info different columns
  gyro = gyro[col].str.split(expand=True).rename(columns={1:"gX",2:"gY",3:"gZ"})
  # clear unnecessary information out
  gyro = gyro.replace([":GyroY:",":gyroZ:"],"",regex= True).iloc[:,1:]
  return gyro


def clean_imudata(df):
    col = sorted(df)[0]
    # Separate Gyro data and Accel data out
    file = df.drop(df[df[col].apply(lambda x: x.startswith('g'))].index).reset_index(drop=True)
    # Split data info into different columns
    file = file[col].str.split(expand=True).rename(columns={1:"time",2:"aX",3:"aY",4:"aZ"})
    # Clear unnecessary characters
    file = file.replace([":accelX:",":accelY:",":accelZ:"],"",regex= True).iloc[:,1:]
    # Clean gyro data
    gyro = clean_gyrodata(df)
    # Concat the Accel & Gyro Data back into one file
    new_df = pd.concat([file,gyro], axis = 1).iloc[:-1,:].dropna()
    return new_df

if __name__ == "__main__":
    file_name, completeName = log_imu_data( )
    df = pd.read_csv(completeName)
    df = clean_imudata(df)
    cleanName = os.path.join(clean_dir, file_name)
    df.to_csv(cleanName)
    print((f"Lengh {len(df)} for the file '{file_name}'."))
    print(df.head())
