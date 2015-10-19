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
    
thumbsize = 50
thumbs = [misc.imresize(x,(thumbsize, thumbsize)) for x in images]

print("Calculating features")
#features = list(map(extractor.calculateNormalizedColorFeatures, images))
angleSplit = 5
angleClasses = 7
colorSplit = 5
colorScale = 80.0
features = numpy.zeros([len(images), angleSplit * angleSplit * angleClasses + colorSplit * colorSplit * 3])
for i in range(amount):
    print(i, "/", amount)
    features[i] = extractor.splitAngleSplitColorFeatures(thumbs[i], angleSplit, angleClasses, 100, colorSplit, colorScale)
    
print("Producing KFold indexes")
kfold = cv.KFold(amount, n_folds = 10, shuffle = True)

print("Evaluating model with KFold")
counter = 0
errors  = numpy.zeros(len(kfold))
wrongs = []
for train_index, test_index in kfold:
    print(counter)
    trainFeatures = [features[i] for i in train_index]
    trainClasses  = [classes[i] for i in train_index]
    testFeatures  = [features[i] for i in test_index]
    testClasses   = [classes[i] for i in test_index]
    
    model = neighbors.KNeighborsClassifier(n_neighbors = 1)
    model.fit(trainFeatures, trainClasses)    
    
    predictedClasses = model.predict(testFeatures)
    errors[counter-1] = errorRate(testClasses, predictedClasses)
    for i in range(len(testClasses)):
        if testClasses[i] != predictedClasses[i]:
            wrongs.insert(0, (predictedClasses[i], testClasses[i]))
    print(errors[counter-1])
    counter = counter + 1
    
wrongDict = dict()
for pred, actual in wrongs:
    if actual in wrongDict:
        wrongDict[actual].insert(0,pred)
    else:
        wrongDict[actual] = [pred]
        
import csv
w = csv.writer(open("wrongs.csv", "w", newline = ''))
for key, val in wrongDict.items():
    row = val.copy()
    row.insert(0,key)
    w.writerow(row)
    
print("mean error ", errors.mean())
print('\a')