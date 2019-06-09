import sklearn.datasets as training_data
import scipy as scipy
import numpy as np
import time

t0 = time.time()


def sigmoid(x, deriv=False):
    if deriv:
        return x*(1-x)
    return 1/(1*(1*np.exp(-x)))


# input data
x = np.array([[0,1,1],
              [1,0,1],
              [1,1,1]])

y = np.array([[0], [1], [1], [0]])

# seed
np.random.seed(1)

# synapse(s)
syn0 = 2*np.random.random((3, 4)) - 1   # (3,4) matrix of random weights with a bias
syn1 = 2*np.random.random((4, 1)) - 1

# Training
for ii in xrange(10000):
    l0 = x
    l1 = sigmoid(np.dot(l0, syn0))    # layer 1
    l2 = sigmoid(np.dot(l1, syn1))    # layer 2

    # back propagation (err reduction)
    l2_err = y - l2

    if ii%1000 == 0:
        print 'Prediction Error: %s ' % str(np.mean(np.abs(l2_err)))

    # deltas for each layer
    l2_delta = l2_err*sigmoid(l2, deriv=True)
    l1_error = l2_delta.dot(syn1.T)
    l1_delta = l1_error * sigmoid(l1, deriv=True)

    # TODO: Learning Rates

    # Update weights (synapses)
    syn1 += l1.T.dot(l2_delta)
    syn0 += l0.T.dot(l1_delta)

print 'Output After Training [%s s Elapsed] ' % (time.time()-t0)
print l2
