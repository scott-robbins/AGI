import pickle
import sys
import os
import time
import numpy as np
import glob
import cv2


def load_dataset(dirpath='cifar-10-batches-py/'):
    """
    this function loads data as numpy array and divides into training set,
    validation set and test set with standardization
    :param dirpath:
    :return:
    """
    X, y = [], []
    # take data from the data batch
    for path in glob.glob('%s/data_batch_*' % dirpath):
        with open(path, 'rb') as f:
            batch = pickle.load(f)  # ,encoding='latin1' (if gives error of encoding)
        X.append(batch['data'])         # append all data and labels from the 5 data batches
        y.append(batch['labels'])

    X = np.concatenate(X) / np.float32(255)                     # divide by 255 for rescaling
    y = np.concatenate(y).astype(np.int32)                      # making labels as int
    X = np.dstack((X[:, :1024], X[:, 1024:2048], X[:, 2048:]))  # separate in to RGB colors
    X = X.reshape((X.shape[0], 32, 32, 3))                      # reshape data into 4D tensor

    Y_train = np.zeros((40000, 10), dtype=np.float32)           # initialize labels
    Y_valid = np.zeros((10000, 10), dtype=np.float32)
    y_test = np.zeros((10000, 10), dtype=np.int32)

    X_train = X[-40000:]        # divide 40000 as training data and it's labels
    y_train = y[-40000:]
    X_valid = X[:-40000]        # divide 10000 as validation data and it's labels
    y_valid = y[:-40000]

    for i in range(40000):      # make training labels for CNN model
        a = y_train[i]
        Y_train[i, a] = 1

    for i in range(10000):      # make validation labels for CNN model
        a = y_valid[i]
        Y_valid[i, a] = 1

    path = '%s/test_batch' % dirpath    # load test set
    with open(path, 'rb') as f:
        batch = pickle.load(f)  # ,encoding='latin1'
    X_test = batch['data'] / np.float32(255)
    X_test = np.dstack((X_test[:, :1024], X_test[:, 1024:2048], X_test[:, 2048:]))
    X_test = X_test.reshape((X_test.shape[0], 32, 32, 3))
    y_t = np.array(batch['labels'], dtype=np.int32)
    # make test labels compatables with CNN model
    for i in range(10000):
        a = y_t[i]
        y_test[i, a] = 1

    # normalize to zero mean and unity variance
    offset = np.mean(X_train, 0)
    scale = np.std(X_train, 0).clip(min=1)
    X_train = (X_train - offset) / scale
    X_valid = (X_valid - offset) / scale
    X_test = (X_test - offset) / scale
    return X_train, Y_train, X_valid, Y_valid, X_test, y_test

t0 = time.time()
x_train, y_train, x_valid, y_valid, x_test, y_test = load_dataset(dirpath='cifar-10-batches-py/')
print '\033[1m* Finished Loading Training Data [%s s Elapsed]\033[0m' % (time.time()-t0)


# Make Sure Everything has correct dims
x_training_shape = np.array(x_train).shape
y_training_shape = np.array(y_train).shape
x_valid_shape = np.array(x_valid).shape
y_valid_shape = np.array(y_valid).shape
x_test_shape = np.array(x_test).shape
y_test_shape = np.array(y_test).shape

n_images = x_training_shape[0]
if n_images != y_training_shape[0]:
    print 'Training Data has dimensions incorrectly configured!'
    exit(0)
if x_valid_shape[0] != y_valid_shape[0]:
    print 'Training Data has dimensions incorrectly configured!'
    exit(0)
if x_test_shape[0] != y_test_shape[0]:
    print 'Training Data has dimensions incorrectly configured!'
    exit(0)

print ' %s Images [%s x %s Each ] ' % (str(x_training_shape[0]),
                                       str(x_training_shape[1]),
                                       str(x_training_shape[2]))
