# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 23:09:33 2015

@author: Rian
"""

from scipy import ndimage
from glob import glob
from pathlib import Path

def extract(filename):
    image = ndimage.imread(filename)
    category = Path(filename).parent.name
    superCategory = Path(filename).parent.parent.name
    return (image, superCategory, category)
    


def loadTrainingImages():
    imagePaths = glob("train/*/*/*.png")
    return list(map(extract, imagePaths))
    

