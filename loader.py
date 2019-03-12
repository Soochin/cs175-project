import torch
from torch.utils.data import DataLoader
import torchvision.transforms as T

import os

from PIL import Image

class HandClassifyDataset(torch.utils.data.Dataset):
  def __init__(self, rootdir):
    self.rootdir = rootdir
    self.handsdir = rootdir+'hands_dataset/'
    self.nohandsdir = rootdir + 'nohands_dataset/'
    self.handIms = []
    self.nohandIms = []
    transform = T.ToTensor()
    i = 0
    for batch in os.listdir(self.handsdir):
      for handFile in os.listdir(self.handsdir+batch):
        self.handIms.append(transform(Image.open(self.handsdir+batch+'/'+handFile)))
        i+= 1
        if i%1000 == 0:
          print(i)
      print('Batch done')
      break
    print('Hands done')
    for batch in os.listdir(self.nohandsdir):
      for nohandFile in os.listdir(self.nohandsdir+batch):
        self.nohandIms.append(transform(Image.open(self.nohandsdir+batch+'/'+nohandFile)))
        i += 1
        if i%1000 == 0:
          print(i)
      print("Batch done")
      break
    print("No Hands done")
    
  def __len__(self):
    #return self._handsLen() + self._nohandsLen()
    return len(self.handIms)+len(self.nohandIms)
  def _handsLen(self):
    return len(self.handIms)

  def _nohandsLen(self):
    return len(self.nohandIms)
  
  def __getitem__(self, idx):
    if idx < len(self.handIms):
      return {"image": self.handIms[idx], "hand":1}
    else:
      idx = idx - len(self.handIms)
      return {"image": self.nohandIms[idx], "hand":0}