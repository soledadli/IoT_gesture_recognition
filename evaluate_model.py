import numpy as np
import pandas as pd

from keras.models import load_model
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.utils import shuffle
from prepare_data import *
from standard import *

model_dir = 'model/'

def softmax_to_one_hot(array):

    i = np.argmax(array)
    one_hot = np.zeros(len(array))
    one_hot[i] = 1
    return one_hot

def one_hot_to_label(array):

    i = np.argmax(array)
    return LABELS_NAMES[i]

def evaluate_model(model, data):
    X_test, y_test = segement_data(
        data[['aX', 'aY', "aZ", "gX", "gY", "gZ"]], data.activity, 5, 1)
    X_test, y_test = shuffle(X_test, y_test, random_state=0)

    # Make predictions
    y_predicted = model.predict(X_test)
    y_predicted = np.asarray([softmax_to_one_hot(y) for y in y_predicted])
    for actual, predicted in zip(y_test, y_predicted):
        print("Actual: ", one_hot_to_label(actual), "\t Predicted: ", one_hot_to_label(predicted))

    return y_predicted, y_test


if __name__ == "__main__":
    test = pd.read_csv(merge_dir + "test.csv")
    model = load_model(model_dir)
    y_predicted, y_test = evaluate_model(model, test)
    print("Final accuracy: ", accuracy_score(y_test, y_predicted))


