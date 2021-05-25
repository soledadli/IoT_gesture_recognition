import pandas as pd
import tensorflow as tf
from tensorflow import keras
from prepare_data import *
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import OneHotEncoder
from sklearn.utils import shuffle


model_dir = 'models/'


def train_lstm_model(X_train,y_train, unit=128, dropout_rate = 0.5):
    model = keras.Sequential()
    model.add(
        keras.layers.Bidirectional(
            keras.layers.LSTM(
                units=unit,
                input_shape=[X_train.shape[1]]
            )
        )
    )
    model.add(keras.layers.Dropout(rate=dropout_rate))
    model.add(keras.layers.Dense(units=unit, activation='relu'))
    model.add(keras.layers.Dense(y_train.shape[1], activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])

    return model


if __name__ == "__main__":
    dfs = pd.read_csv("merge_data/scaled_data/scaled_test0.csv")
    X, y = segement_data(
        dfs[['aX', 'aY', "aZ", "gX", "gY", "gZ"]], dfs.activity,5, 1)
    X_train, X_test, y_train, y_test = split_data(X, y)
    y_train, y_test, enc = encode_data(y_train, y_test)
    model = train_lstm_model(X_train,y_train)
    history = model.fit(
        X_train, y_train,
        epochs=10,
        batch_size=45,
        validation_split=0.2)
    model.save('models/lstm_model.h5')

    score = model.evaluate(X_test, y_test, verbose=0)
    print(f'Test loss: {score[0]} / Test accuracy: {score[1]}')
    predictions = model.predict(X_test)
    category = np.argmax(predictions, axis=1)
    print("categorization: ", category)

