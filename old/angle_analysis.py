# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 23:58:29 2015

@author: Rian

Shows why normalizing colors before using them is interesting.
It helps for images taken in different lighting conditions.
First the script shows a dark and normal image without normalization
and with normalization. Then it shows that normalization produces better
clustering when used as features of the data set.

TODO: name some more stuff
"""

from scipy import ndimage
import data_loading as loader
import feature_extraction as extractor
from matplotlib import pyplot as plot
from mpl_toolkits.mplot3d.axes3d import Axes3D

darkImage = ndimage.imread("train/diamonds/B9/00585_09701.png")
normalImage = ndimage.imread("train/diamonds/B9/00042_00233.png")
playImage = ndimage.imread("train/rectangles_down/F12a/00441_02146.png")
circleImage = ndimage.imread("train/red_circles/C3/01312_08809.png")
squareImage = ndimage.imread("train/squares/F19/00817_05499.png")

images = loader.loadTrainingImages()

classA = list(filter(lambda i: i[2] == "D1a", images))
classB = list(filter(lambda i: i[2] == "B9", images))
classC = list(filter(lambda i: i[2] == "B5", images))

fig = plot.figure()
axes = fig.add_subplot(1,2,1, projection = '3d', title = 'Using Colors', xlabel = 'Red Mean', ylabel = 'Green Mean', zlabel = 'Blue Mean')

def plotFeatures(axes, data, featureFunction, amount, color, marker, label = ''):  
    counter = 0
    for image in data[0:amount]:
        print(counter)
        counter+=1
        colorFeatures = featureFunction(image[0])
        axes.scatter(colorFeatures[0],colorFeatures[1],colorFeatures[2], c=color, marker=marker)
    axes.plot([], [], marker, c=color, label=label)

def compose(f,g):
    return lambda x: f(g(x))

plotFeatures(axes, classA, extractor.angleFeatures, -1, 'r', 'o', 'D1a')
plotFeatures(axes, classB, extractor.angleFeatures, -1, 'b', '^', 'B9')
plotFeatures(axes, classC, extractor.angleFeatures, -1, 'g', 'x', 'B5')
axes.legend(loc = 0, scatterpoints = 1)