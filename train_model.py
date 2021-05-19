import pandas as pd
import tensorflow as tf
from tensorflow import keras
from prepare_data import *
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import OneHotEncoder

model_dir = 'model/'



def train_lstm_model(X_train,y_train):
    model = keras.Sequential()
    model.add(
        keras.layers.Bidirectional(
            keras.layers.LSTM(
                units=128,
                input_shape=[X_train.shape[1]]
            )
        )
    )
    model.add(keras.layers.Dropout(rate=0.5))
    model.add(keras.layers.Dense(units=128, activation='relu'))
    model.add(keras.layers.Dense(y_train.shape[1], activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])

    return model

def visualize_loss(history):
    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='test')
    plt.legend()


def plot_cm(inverse_encode_y_true, inverse_encode_y_pred, class_names):
  cm = confusion_matrix(inverse_encode_y_true, inverse_encode_y_pred)
  fig, ax = plt.subplots(figsize=(18, 16))
  ax = sns.heatmap(
      cm,
      annot=True,
      fmt="d",
      cmap=sns.diverging_palette(220, 20, n=7),
      ax=ax
  )

  plt.ylabel('Actual')
  plt.xlabel('Predicted')
  ax.set_xticklabels(class_names)
  ax.set_yticklabels(class_names)
  b, t = plt.ylim() # discover the values for bottom and top
  b += 0.5 # Add 0.5 to the bottom
  t -= 0.5 # Subtract 0.5 from the top
  plt.ylim(b, t) # update the ylim(bottom, top) values
  plt.show() # ta-da!


if __name__ == "__main__":
    dfs = pd.read_csv("merge_data/scaled_data/scaled_test0.csv")
    X, y = segement_data(
        dfs[['aX', 'aY', "aZ", "gX", "gY", "gZ"]],
        dfs.activity,
        5,
        1
    )
    X_train, X_test, y_train, y_test = split_data(X,y)
    y_train, y_test, enc = encode_data(y_train, y_test)
    model = train_lstm_model(X_train,y_train)
    history = model.fit(
        X_train, y_train,
        epochs=10,
        batch_size=45,
        validation_split=0.2)
    model.save(model_dir)
    y_pred = model.evaluate(X_test, y_test)
    print(y_pred)
'''
    plot_cm(
        enc.inverse_transform(y_test),
        enc.inverse_transform(y_pred),
        enc.categories_[0]
    )
        
'''
