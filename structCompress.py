import os
import sys
import csv
from tqdm import tqdm
from config import *


if __name__ == '__main__':
    nodeMap = {}  # 为每个节点构建入边映射
    edgeMap = {}
    newEdges = []
    newNodes = []

    with open(os.path.join(csv_dir, edge_csv_file), 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        edgeIndex = 1
        for edge in reader:  # edge: [u,v, type, time]
            if edge[1] not in nodeMap.keys():
                nodeMap[edge[1]] = [] # nodeMap: {v:u}
            nodeMap[edge[1]].append(edge[0])
    
    for v in nodeMap.keys():
        newEdge = []
