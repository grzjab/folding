import matplotlib.pyplot as plt
import numpy as np

def plot_signature( signature ) :
    plt.figure()
    x,y = np.where( signature>0 )
    plt.scatter(x,y, )#np.reshape(s,(-1)))
    plt.show()
