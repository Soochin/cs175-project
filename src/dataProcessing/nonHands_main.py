import os
import sys
import io
import random
from PIL import Image, ImageChops
import urllib2 as urllib

FINAL_IMAGE_DIM = 256
HANDS_PATH = './hands_dataset/'
IMNET_PATH = './fall11_urls.txt'
OUTPUT_PATH = './nohands_dataset/'

def getHandsSize():
    return len(os.listdir(HANDS_PATH))

def readImNet():
    f = open(IMNET_PATH)
    lines = f.readlines()
    f.close()
    lines = [l.rstrip('\n') for l in lines]
    return lines

def getImNetUrls(previousUrls):
    urls = []
    samples = readImNet()
    for s in samples:
        s = s.split('\t')
        wnid = s[0].split('_')
        if (s[1], wnid[0]) not in previousUrls:
            urls.append((s[1], wnid[0]))
    random.shuffle(urls)
    return list(previousUrls)+urls

def getImages(urls, maxCount, skip):
    noLongerAvailable = Image.open('./noImageAvailable.png').convert('RGB')
    images = []
    goodUrls = []
    count = 0
    failCount = 0
    for url, wnid in urls:
        if skip > 0:
            skip -=1
            count += 1
            goodUrls.append((url, wnid))
            continue
        try:
            print("Trying Url: " + url)
            fd = urllib.urlopen(url)
            print("\tReading Bytes...")
            image_file = io.BytesIO(fd.read())
            print("\tOpening Image...")
            im = Image.open(image_file).convert('RGB')
            print("\tDetecting No Longer Available...")
            if ImageChops.difference(im, noLongerAvailable).getbbox() == None:
                raise
            print("\t Appending Image")
            images.append(im)
        except:
            failCount += 1
            print("\tFailed Url(" + str(failCount) + "): " +url)
        else:
            count += 1
            print(count)
            goodUrls.append((url, wnid))
            if count % 100 == 0:
                writeGoodUrls(goodUrls)
                if count < maxCount:
                    transformAndSave(images, count)
                images = []
            
    return images

def writeGoodUrls(urls):
    f = open('noHands.txt', 'w')
    for url in urls:
        f.write(url[0]+'\t' + url[1] + '\n')
    f.close()

def saveImageFile(image, fileName, extension):
    if(image.size[0] == FINAL_IMAGE_DIM and image.size[1] == FINAL_IMAGE_DIM):
        image.save(fileName, extension)

def saveImages(images, group):
    for i in range(len(images)):
        saveImageFile(images[i],OUTPUT_PATH +str(group+i)+'.jpg', 'JPEG')
        
def transformImage(image):
    if image.size[0] < image.size[1]:
        #portrait orientation
        scale = float(FINAL_IMAGE_DIM)/image.size[0]
    else:
        scale = float(FINAL_IMAGE_DIM)/image.size[1]
    im = image.resize((int(image.size[0]*scale), int(image.size[1]*scale)))
    width = im.size[0]
    height = im.size[1]
    left = int((width-FINAL_IMAGE_DIM)/2)
    top = int((height-FINAL_IMAGE_DIM)/2)
    im = im.crop((left,top,left+FINAL_IMAGE_DIM, top+FINAL_IMAGE_DIM))
    return im

def transformImages(images):
    result = []
    for image in images:
        result.append(transformImage(image))
    return result

def transformAndSave(images, group):
    images = transformImages(images)
    saveImages(images, group)

def getPreviousUrls():
    result = set()
    f = open('noHands.txt')
    for line in f.readlines():
        image = line.rstrip('\n').split('\t')
        result.add((image[0], image[1]))
    f.close()
    return result
    
if __name__ == "__main__":  
    previousUrls = getPreviousUrls()
    print(len(previousUrls))
    count = getHandsSize()
    print(count)
    urls = getImNetUrls(previousUrls)
    print(len(urls))
    getImages(urls, count, len(previousUrls))
    #transformAndSave(images)