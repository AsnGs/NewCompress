import os
import csv
from config import *
from utils import *


def mergeEdges(edgeList, nodeIndex, v):
    if len(edgeList) == 1 : return edgeList[0]
    mergedEdge = [nodeIndex, v]
    startTime, endTime = sys.maxsize, 0
    for edges in edgeList:
        for edge in edges:
            if edge[1] > endTime: endTime = edge[1]
            if edge[1] < startTime: startTime = edge[1]


if __name__ == '__main__':
    os.makedirs(sc_dir, exist_ok=True)

    vertexMap = {} # vertexMap : {v:u}
    edgeMap = {} # edgeMap : {(u, v): e} 
    newEdges = []
    newVertex = []

    mergeVertexDict = {}
    medgeEdgeDict = {}

    with open(os.path.join(csv_dir, edge_csv_file), 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        for edge in reader:  # edge: [u,v, type, time]
            if edge[1] not in vertexMap.keys():
                vertexMap[edge[1]] = [] #
            vertexMap[edge[1]].append(edge[0])
            if (edge[0], edge[1]) not in edgeMap.keys():  
                edgeMap[(edge[0], edge[1])] = []
            edgeMap[(edge[0], edge[1])].append(edge[2:])
                
    nodeIndex = 0
    edgeIndex = 0
    for v in vertexMap.keys():
        U = vertexMap[v]
        mergeVertexDict[nodeIndex] = U
        tmpMergeEdges = [edgeMap[(u, v)] for u in U]
        mergedEdge = mergeEdges(tmpMergeEdges, nodeIndex, v)

