import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
import seaborn as sns
from pylab import rcParams
import matplotlib.pyplot as plt
from sklearn.preprocessing import RobustScaler

scaled_dir = "merge_data/scaled_data/"

# Scaling the data to emphasize difference
def scale_data(df, file_name):
    scale_columns = ['aX', 'aY', 'aZ',"gX","gY","gZ"]
    scaler = RobustScaler()
    scaler = scaler.fit(df[scale_columns])
    df.loc[:, scale_columns] = np.round(scaler.transform(df[scale_columns].to_numpy()), 3)
    df.to_csv(scaled_dir + "scaled_"+ file_name + ".csv")
    return df

if __name__ == "__main__":
    df= pd.read_csv("merge_data/test0.csv", index_col=[0])
    dfs =scale_data(df, "test0")
    print(dfs.head())