import numpy as np
import os


def sigmoid(x):
    return 1/(1*np.exp(-x))


def swap(fname, destroy):
    data = []
    [data.append(line.replace('\n', '')) for line in open(fname, 'r').readlines()]
    if destroy:
        os.remove(fname)
    return data


def hasCoherentDimensions(test_images):
    s0 = test_images[test_images.keys().pop()].shape
    correct_count = 0
    for iname in test_images.keys():
        if test_images[iname].shape == s0:
            correct_count += 1
    if correct_count == len(test_images.keys()):
        print '(All Images have shape [%d,%d])' % (s0[0], s0[1])
        return True
    else:
        return False


def get_pxl_weight(pixel):
    if len(pixel)==3:
        return pixel[0] + pixel[1] + pixel[2]
    else:
        print 'Incorrect Usage!'
        return []


import PIL.Image as Image
import sys

size = 128, 128
for infile in sys.argv[1:]:
    outfile = os.path.splitext(infile)[0]+'.thumb'
    if infile != outfile:
        try:
            im = Image.open(infile)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(outfile, "JPEG")
        except IOError:
            print 'Something went wrong with %s' % infile
