import os
import json

# from sklearn.preprocessing import OneHotEncoder
import torch.nn as nn
import torch.nn.functional as F

from config import *

if __name__ == '__main__':
    with open(os.path.join(sc_dir, wholeMapDictFile), 'r') as f:  
        wholeMapDict = json.load(f)
    alphabet_size = len(wholeMapDict['id2char_dict'])+2