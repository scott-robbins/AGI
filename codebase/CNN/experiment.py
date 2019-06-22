import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import scipy.misc
import numpy as np
import os


def initialize_image_library():
    if not os.path.isdir('alphabet'):
        cmd = 'mkdir alphabet; cd alphabet; ' \
              'sftp pi@192.168.1.229:/media/pi/9802-3A2C/TylersDurden/WeekendWarrior/RPI/Vision/alphabet/*'
        os.system(cmd)
    return True


def extract(letters):
    return letters[220:380, 220:365]


has_photos = initialize_image_library()
imgs = os.listdir('alphabet')

images = []
for img in imgs:
    images.append(extract(plt.imread('alphabet/' + img)))
print str(len(images)) + ' Images loaded'
iex = images[6]

imean = iex -ndi.mean(iex)

plt.imshow(imean, 'gray')
plt.show()
