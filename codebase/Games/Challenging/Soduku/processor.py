import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import scipy.misc
import sys
import os

if len(sys.argv) ==2:
    im = np.array(scipy.misc.imread(sys.argv[1]))
    print im.shape
    plt.imshow(np.rot90(np.rot90(np.rot90(im))))
    plt.show()

    # Find the squares first

