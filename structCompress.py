import os
import csv
from config import *
from utils import *


def mergeEdges(edgeList, nodeIndex, v):
    if len(edgeList) == 1 : return edgeList[0]
    mergedEdge = [nodeIndex, v]  # [merged]
    times = sorted(list(set([int(e[1]) for edges in edgeList for e in edges])))
    # startTime, endTime = min(times), max(times)
    mergedEdge.extend([times[0], times[-1]])  

    specificContent = {}  # {timeOffset: [vertexOffset, type]}  #!  vertexOffset -> vertexIndex better?

    for i in range(len(edgeList)):
        for j in range(len(edgeList[i])):
            offsetTime = int(edgeList[i][j][1]) - minsTime #  offset
            if offsetTime not in specificContent.keys(): specificContent[offsetTime] = []
            specificContent[offsetTime].append([i, rel2id[edgeList[i][j][0]]])
    mergedEdge.append(specificContent)
    return mergedEdge





if __name__ == '__main__':
    os.makedirs(sc_dir, exist_ok=True)

    vertexMap = {} # vertexMap : {v:u}
    edgeMap = {} # edgeMap : {(u, v): e} 
    newEdges = []
    newVertex = []

    mergedIndex2allVertexs = {}  # merged Vertex Index to u (one to many)
    vertex2mergedIndex = {}  # vertex to merged Vertex Index (one to many)
    medgeEdgeDict = {}

    with open(os.path.join(csv_dir, edge_csv_file), 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        for edge in reader:  # edge: [u,v, type, time]
            if edge[1] not in vertexMap.keys():
                vertexMap[edge[1]] = [] 
            vertexMap[edge[1]].append(edge[0])
            if (edge[0], edge[1]) not in edgeMap.keys():  
                edgeMap[(edge[0], edge[1])] = []
            if edge[2:] not in edgeMap[(edge[0], edge[1])]:  # src,dst,type,time 完全相同就按一个算了
                edgeMap[(edge[0], edge[1])].append(edge[2:])
                
    nodeIndex = 0
    edgeIndex = 0
    for v in vertexMap.keys():
        if len(vertexMap[v]) == 1:
            u = vertexMap[v][0]
            timestamp = edgeMap[(vertexMap[v][0], v)][0][1]
            edgeType  = edgeMap[(vertexMap[v][0], v)][0][0]
            newEdges.append([u, v, timestamp, timestamp, {(int(timestamp)-minsTime): [[0, rel2id[edgeType]]]} ])
            continue

        U = vertexMap[v]
        mergedIndex2allVertexs[nodeIndex] = U
        tmpMergeEdges = [edgeMap[(u, v)] for u in U]
        mergedEdge = mergeEdges(tmpMergeEdges, nodeIndex, v)
        newEdges.append(mergedEdge)
        for u in U:
            if u not in vertex2mergedIndex.keys(): vertex2mergedIndex[u] = []
            vertex2mergedIndex[u].append(nodeIndex)
            
        nodeIndex += 1
    
    print('a')

