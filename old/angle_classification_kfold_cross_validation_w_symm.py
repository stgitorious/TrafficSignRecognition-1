# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 15:01:46 2015

@author: Rian
"""

import data_loading as loader
import feature_extraction as extractor
import image_operations as operations
import sklearn.cross_validation as cv
import numpy
from scipy import misc
from scipy import stats
from sklearn import neighbors

def distance(a,b):
    return numpy.sum(numpy.square(numpy.add(a, numpy.multiply(b, -1))))
    
def errorRate(a,b):
    return numpy.sum(numpy.array(a) != numpy.array(b)) / len(a)

def nearestNeighbour(xs, ys, x):
    bestIndex = 0
    bestDistance = distance(xs[0],x)
    for i in range(len(xs)):
        d = distance(xs[i], x)
        if d < bestDistance:
            bestIndex = i
            bestDistance = d
    return ys[bestIndex]
    
def kNearestNeighbour(k, xs, ys, x):
    distances = [distance(x, i) for i in xs] 
    indexes = numpy.argsort(distances)
    classes = [ys[indexes[i]] for i in range(k)]
    return stats.mode(classes)[0][0]

print("Loading images")
images, classes = loader.loadTrainingAndClasses()
amount = len(images)

print("Making thumbnails")
def resizeProper(image, maxPixels):
    ratio = len(image) / len(image[0])
    height = int(numpy.sqrt(maxPixels / ratio))
    width = int(ratio * height)
    return misc.imresize(image, (width, height))
    
thumbsize = 25;
thumbs = [misc.imresize(x,(thumbsize,thumbsize)) for x in images]

print("Calculating features")
#features = list(map(extractor.calculateNormalizedColorFeatures, images))
angleclasses = 15 #deviding 2pi into this many equal classes
symmetryfeatures = numpy.zeros([len(images), angleclasses*4])   #to calculate the features on quadrants of the image

for i in range(amount):
    print(i, "/", amount)
    for quadrant in range(4):
        horizontal = quadrant % 2       #0 or 1 for which horizontal quadrant
        vertical = (quadrant / 2 ) >= 1 #0 or 1 for which vertical quadrant
        size = thumbsize/2
        subthumb = thumbs[i][horizontal*size:(horizontal+1)*size,vertical*size:(vertical+1)*size,:]
        symmetryfeatures[i][quadrant*angleclasses:(quadrant+1)*angleclasses] = extractor.angleFeatures(subthumb, angleclasses)
    
print("Producing KFold indexes")
kfold = cv.KFold(amount, n_folds = 10, shuffle = True)

print("Evaluating model with KFold")
counter = 0
errors  = numpy.zeros(len(kfold))
for train_index, test_index in kfold:
    print(counter)
    trainFeatures = [symmetryfeatures[i] for i in train_index]
    trainClasses  = [classes[i] for i in train_index]
    testFeatures  = [symmetryfeatures[i] for i in test_index]
    testClasses   = [classes[i] for i in test_index]
    
    model = neighbors.KNeighborsClassifier(n_neighbors = 1)
    model.fit(trainFeatures, trainClasses)    
    
    predictedClasses = model.predict(testFeatures)
    #predictedClasses = [kNearestNeighbour(10, trainFeatures, trainClasses, x) for x in testFeatures]
    errors[counter-1] = errorRate(testClasses, predictedClasses)
    print(errors[counter-1])
    counter = counter + 1
    
print("mean error ", errors.mean())
print('\a')