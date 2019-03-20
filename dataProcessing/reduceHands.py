import os
import random
import math
from PIL import Image

HANDS_PATH = './hands_dataset_21100/'
NOHANDS_PATH = './nohands_dataset/'
FINAL_FOLDER_COUNT = 5

def copyImages(paths, folderCount):
    i=0
    for f in paths:
        image = Image.open(NOHANDS_PATH + f)
        image.save('./nohands_dataset_'+str(folderCount)+'/'+f, 'JPEG')
        image.close()
        i += 1
        print('\t'+str(i))

def getPaths(paths):
    for i in range(FINAL_FOLDER_COUNT-1):
        print(i)
        copyImages(paths[int(i*math.ceil(len(paths)/FINAL_FOLDER_COUNT)):int((i+1)*math.ceil(len(paths)/FINAL_FOLDER_COUNT))], i)
    print(FINAL_FOLDER_COUNT-1)
    copyImages(paths[int((FINAL_FOLDER_COUNT-1)*math.ceil(len(paths)/FINAL_FOLDER_COUNT)):], FINAL_FOLDER_COUNT-1)

if __name__ == "__main__":
    hands = os.listdir(NOHANDS_PATH)
    print(len(hands))
    getPaths(hands)
    
