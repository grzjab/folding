#from __future__ import print_function
import collections
import math
import numpy as np
import os
import random
import tensorflow as tf

#import seaborn as sns
from scipy.sparse import lil_matrix
import pickle
from tfSom import SOM
from textProcessing import *
from utility import *

url = 'http://mattmahoney.net/dc/'
filename = maybe_download('text8.zip', 31344016)

words = read_data(filename)
print('Data size %d' % len(words))
print(len(set(words)))

vocabulary_size = 5000

data, count, dictionary, reverse_dictionary = build_dataset(words, vocabulary_size)
print('Most common words (+UNK)', count[:5])
print('Sample data', data[:10])
del words  # Hint to reduce memory.

window_size = 2
train_data = build_contexts(window_size, data, dictionary)

dict_size = len(dictionary)
d = 16


som = SOM(d, d, dict_size, n_iterations = 100, batch_size=1000)
som.train(train_data)
som.save("som.pkl")

