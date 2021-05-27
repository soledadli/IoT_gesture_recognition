import pandas as pd
import numpy as np
import seaborn as sns
from pylab import rcParams
import matplotlib.pyplot as plt
from sklearn.preprocessing import RobustScaler
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder


scaled_dir = "data_pipeline/merge_data/scaled_data/"
TIME_STEPS = 5
STEP = 1

# Scaling the data to emphasize difference
def scale_data(df, file_name):
    scale_columns = ['aX', 'aY', 'aZ',"gX","gY","gZ"]
    scaler = RobustScaler()
    scaler = scaler.fit(df[scale_columns])
    df.loc[:, scale_columns] = np.round(scaler.transform(df[scale_columns].to_numpy()), 3)
    df.to_csv(scaled_dir + "scaled_"+ file_name + ".csv")
    return df

def segement_data(feature, label, time_steps=5, step=1):
    Xs, ys = [], []
    for i in range(0, len(feature) - time_steps, step):
        v = feature.iloc[i:(i + time_steps)].values
        labels = label.iloc[i: i + time_steps]
        Xs.append(v)
        ys.append(stats.mode(labels)[0][0])
    return np.array(Xs), np.array(ys).reshape(-1, 1)

def split_data(feature,label):
    X_train, X_test, y_train, y_test = train_test_split(feature, label, test_size=0.2, random_state=4, stratify=label)
    return X_train, X_test, y_train, y_test

def encode_data(y_train, y_test):
    enc = OneHotEncoder(handle_unknown='ignore', sparse=False)
    enc = enc.fit(y_train)
    y_train = enc.transform(y_train)
    y_test = enc.transform(y_test)
    print(enc.categories_)
    return y_train, y_test

if __name__ == "__main__":
    df= pd.read_csv("data_pipeline/merge_data/test0.csv", index_col=[0])
    dfs =scale_data(df, "test0")
    X, y = segement_data(
        dfs[['aX', 'aY', "aZ", "gX", "gY", "gZ"]],
        dfs.activity,
        TIME_STEPS,
        STEP
    )

    X_train, X_test, y_train, y_test = split_data(X,y)
    y_train, y_test = encode_data(y_train, y_test)

   # print(X_train.shape, y_train.shape) # y_train is the encoded label, in form with [0,1]

