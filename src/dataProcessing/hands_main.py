import os
import sys
import random
import urllib2
from scipy.io import loadmat
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image



FINAL_IMAGE_DIM = 256;
BASE_PATH = './oxford_dataset/training_dataset/training_data/'
IMAGE_PATH = BASE_PATH + 'images/'
ANNOTATION_PATH = BASE_PATH+'annotations/'
OUTPUT_PATH = './hands_dataset/'

class handBox():
    def __init__(self, minX, minY, maxX, maxY):
        self.minX = minX
        self.minY = minY
        self.maxX = maxX
        self.maxY = maxY
    
    def resize(self, xScale, yScale):
        minX = self.minX * xScale
        maxX = self.maxX * xScale
        minY = self.minY * yScale
        maxY = self.maxY * yScale
        return handBox(minX, minY, maxX, maxY)
        
    def shiftWithCrop(self, bbox):
        minX = self.minX - bbox[0]
        maxX = self.maxX - bbox[0]
        minY = self.minY - bbox[1]
        maxY = self.maxY - bbox[1]
        return handBox(minX, minY, maxX, maxY)
    
    def getDims(self):
        return (self.maxX-self.minX, self.maxY-self.minY)
          
    def __repr__(self):
        return "["+str(self.minX)+"-"+ str(self.maxX)+ ", " +str(self.minY)+ "-"+ str(self.maxY)+"]"
    def __str__(self):
        return self.__repr__()

def findAllFiles(filePath, extension):
    result = []
    for file in os.listdir(filePath):
        f = file.split('.')
        if(f[1] == extension):
            result.append(f[0])
    return result

def saveImageFile(image, fileName, extension):
    if(image.size[0] == FINAL_IMAGE_DIM and image.size[1] == FINAL_IMAGE_DIM):
        image.save(fileName, extension)

def saveImages(images, fileName, limit):
    if limit and limit <len(images):
        images = random.sample(images, limit)
    for i in range(len(images)):
        saveImageFile(images[i],OUTPUT_PATH +fileName+'_'+str(i)+'.jpg', 'JPEG')

def openImageFile(filePath):
    im = Image.open(filePath)
    #plt.imshow(im)
    #plt.show()
    return im
        
def getFullHand(image, handbox):
    handDims = handbox.getDims()
    xScale = FINAL_IMAGE_DIM / handDims[0]
    newWidth = image.size[0]*xScale
    yScale = FINAL_IMAGE_DIM / handDims[1]
    newHeight = image.size[1]*yScale
    image = image.resize((int(newWidth), int(newHeight)), Image.ANTIALIAS)
    hb = handbox.resize(xScale, yScale)
    return image.crop((hb.minX, hb.minY, hb.maxX, hb.maxY))
    
def getImageConvolution(image, handbox):
    results = []
    right = handbox.maxX
    left = right-FINAL_IMAGE_DIM
    bottom = handbox.maxY
    top = bottom - FINAL_IMAGE_DIM
    width = image.size[0]
    height = image.size[1]
    while top <= handbox.minY and bottom < height:
        while left <= handbox.minX and right < width:
            if(left >=0 and top >= 0):
                results.append(image.crop((left, top, right, bottom)))
            left += 8
            right += 8
        top += 8
        bottom += 8
        left = right-FINAL_IMAGE_DIM
        right = handbox.maxX
    return results
    
    
def readAnnoFile(filePath):
    result = []
    m = loadmat(filePath)
    for box in m['boxes'][0]:
        minX = sys.maxint
        minY = sys.maxint
        maxX = -sys.maxint - 1
        maxY = -sys.maxint - 1
        for i in ['a', 'b', 'c', 'd']:
            point = box[i][0][0][0]
            if point[0] > maxY:
                maxY = point[0]
            if point[0] < minY:
                minY = point[0]
            if point[1] > maxX:
                maxX = point[1]
            if point[1] < minX:
                minX = point[1]
        result.append(handBox(minX, minY, maxX, maxY))
    return result

def displayImage(image):
    plt.figure
    plt.imshow(image)
    plt.show()

def resize(image, handBox, i):
    xScale = (i*.5)+1
    yScale = (i*.5)+1
    newWidth = image.size[0]*xScale
    newHeight = image.size[1]*yScale
    im = image.resize((int(newWidth), int(newHeight)), Image.ANTIALIAS)
    hb = handBox.resize(xScale, yScale)
    return (im, hb)
    
def processHand(image, handBox):
    results = []
    cIm = getImageConvolution(image, handBox)
    results += cIm
    i=1
    while len(cIm)>0:
        im, hb = resize(image, handBox, i)
        cIm = getImageConvolution(im, hb)
        results += cIm
        i+=1.25
    return results

def cropBorder(image, handBoxes):
    finalHBs = []
    border = image.getbbox()
    for hb in handBoxes:
        hb = hb.shiftWithCrop(border)
        finalHBs.append(hb)
    im = image.crop(border)
    return (im, finalHBs)

def processImage(image, handBoxes):
    results = []
    #image, handBoxes = cropBorder(image, handBoxes)    
    print(image.size)
    for hb in handBoxes:
        print("New Hand")
        results += processHand(image, hb)
        print(len(results))
    return results
    
if __name__ == "__main__":
    imageFiles = findAllFiles(IMAGE_PATH, 'jpg')
    print(len(imageFiles))
    j = 1
    for imageFile in imageFiles:
        if("Buffy" in imageFile):
            continue
        print('Image #'+str(j)+imageFile)
        handBoxes = readAnnoFile(ANNOTATION_PATH+imageFile+'.mat')
        image = openImageFile(IMAGE_PATH + imageFile+'.jpg')
        finalImages = processImage(image, handBoxes)
        saveImages(finalImages, imageFile, 10)


#Buffy is breaking because most of the original images contain a black border
#look at using im.getbbox to preprocess crop these.