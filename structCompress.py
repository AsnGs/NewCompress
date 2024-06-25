import os
import sys
import csv
from tqdm import tqdm
from config import *


if __name__ == '__main__':
    nodeMap = {}
    edgeMap = {}

    with open(os.path.join(csv_dir, vertex_csv_file), 'r') as csvfile:
        reader = csv.reader(csvfile)
        vertexData = list(reader)