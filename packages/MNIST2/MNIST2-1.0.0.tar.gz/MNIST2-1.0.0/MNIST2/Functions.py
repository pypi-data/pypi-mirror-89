# Functions

import numpy as np
from PIL import Image

def func(x):
    #return -np.log(x*(-1)/255.1 + 1)
    return - 1/ ((1 * x/256)-1) - 1

def sigmoid(x):
    return 1/(1+np.exp(-x))

def penalty(X):
    return None

def bias(x):
    return 128*np.sin(3.1415/256*x-3.1415/2) + 128

def antibias(x):
    return 256/3.1415*(np.arcsin(x/128 - 1)) + 128

def show(array):
    img = Image.fromarray(array)
    img.show()

# WSG suanfa
def generalization(array):
    x0, x1, x2, x3, x4 = 4, 1, 1, 1, 1
    add = (x0+x1+x2+x3+x4)/2
    array0 = array[1:-1, 1:-1]
    array1 = x0*array0 + x1*array[:-2, 1:-1] + x2*array[2:, 1:-1] + x3+array[1:-1, :-2] + x4*array[1:-1, 2:]
    array2 = np.vstack((np.zeros(26), array1, np.zeros(26)))
    Array = np.hstack((np.zeros(28).reshape(28, 1), array2, np.zeros(28).reshape(28, 1)))
    return Array 
