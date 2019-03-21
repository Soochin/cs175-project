import cv2
import skin_detector
import os
from PIL import Image

BASE_PATH = 'C:\\Users\\vic07\\OneDrive\\Documents\\College\\Year_4\\Winter\\CS175\\FinalProject\\Data\\HandData\\nohands_dataset_128\\'
imgFiles = os.listdir(BASE_PATH)

for img in imgFiles:
    print(img)
    if("Buffy" in img):
        continue
    path = BASE_PATH + img
    image = cv2.imread(path)
    mask = skin_detector.process(image)
    idx=(mask==0)
    image[idx]=0
    #cv2.imshow("input", image)
    #cv2.waitKey(0)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(image, 'RGB')
    im.save('C:\\Users\\vic07\\OneDrive\\Documents\\College\\Year_4\\Winter\\CS175\\FinalProject\\Data\\HandData\\skin_detected_nohands_128\\'+img, 'JPEG')
    