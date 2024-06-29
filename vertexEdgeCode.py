import os
import csv
import pickle
from config import *
from utils import *

if __name__ == '__main__':

    # read in newedges
    with open(os.path.join(sc_dir, 'newEdges.pkl'), 'rb') as f:
        newEdges = pickle.load(f)

    
