import os
import sys
import io
import random
from PIL import Image, ImageChops


FINAL_IMAGE_DIM = 128
INPUT_PATH = './nohands_dataset_0/'
OUTPUT_PATH = './nohands_dataset_128/'
    

if __name__ == "__main__":
    i = 0
    files = os.listdir(INPUT_PATH)
    for fileName in files:
        img = Image.open(INPUT_PATH+fileName)
        im = img.resize((FINAL_IMAGE_DIM, FINAL_IMAGE_DIM), Image.ANTIALIAS)
        im.save(OUTPUT_PATH+fileName, 'JPEG')
        i += 1
        print(i)