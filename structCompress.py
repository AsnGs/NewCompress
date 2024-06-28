import os
import csv
import pickle
from config import *
from utils import *

# # return content
# def consAndCodeContent(edgeList):
#     content = {} # content: {offsetTime:{typeIndex:[vertexOffset]}}
#     for i in range(len(edgeList)):
#         for j in range(len(edgeList[i])):
#             offsetTime = int(edgeList[i][j][1]) - minsTime #  offset
#             typeIndex = rel2id[edgeList[i][j][0]]
#             if offsetTime not in content.keys(): content[offsetTime] = []
#             content[offsetTime].append([i, typeIndex])
#     return content

def consAndCodeContent(edgeList):
    content = {} # content: {offsetTime:{typeIndex:[vertexOffset]}}   # 多重字典嵌套
    for i in range(len(edgeList)):
        for j in range(len(edgeList[i])):
            offsetTime = int(edgeList[i][j][1]) - minsTime #  offset
            typeIndex = rel2id[edgeList[i][j][0]]
            if offsetTime not in content.keys(): content[offsetTime] = {}
            if typeIndex not in content[offsetTime].keys(): content[offsetTime][typeIndex] = []
            content[offsetTime][typeIndex].append(i)
    return content

# 本来是将单 u 的节点不合并不映射，放在外面处理了，但是考虑后还是将其统一了，同时也映射，算src 部分的编码了
def mergeEdges(edgeList, mergedVetexIndex, v):
    mergedEdge = [mergedVetexIndex, v]  # [merged]
    times = sorted(list(set([int(e[1]) for edges in edgeList for e in edges])))
    # startTime, endTime = min(times), max(times)
    if len(edgeList) == 1:
        mergedEdge.extend([times[0]-minsTime, times[0]-minsTime])
    else:
        mergedEdge.extend([times[0]-minsTime, times[-1]-minsTime])  

    specificContent = consAndCodeContent(edgeList)
    mergedEdge.append(specificContent)
    return mergedEdge

def getFieldValueIndex_MappingDict(jsonObj, mapDict, mins):
    for i in range(len(jsonObj)):
        tempField = list(jsonObj.keys())[i]
        tempValue = jsonObj[tempField]
        if tempField == 'starttime':
            continue
        if tempField == 'endtime':
            continue
        else:
            if tempField not in mapDict.keys():
                mapDict[tempField] = {}
            if tempValue not in mapDict[tempField].keys():
                mapDict[tempField][tempValue] = len(mapDict[tempField].keys())  # {field: {value: index}}
    return mapDict



if __name__ == '__main__':
    os.makedirs(sc_dir, exist_ok=True)

    vertexMap = {} # vertexMap : {v:u}
    edgeMap = {} # edgeMap : {(u, v): e} 
    newEdges = [] # [[dst, starttime, endtime]]

    mergedIndex2us = {}  # merged Vertex Index to u (one to many)  {i:[u1, u2, ...]}
    u2mergedIndex = {}  # vertex to merged Vertex Index (one to many) {u:[i1, i2, ...]}
    mergedIndex2content = {} # merged Vertex Index to its responding content {i1:content1, ...]}

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
                
    mergedVetexIndex = 0
    for v in vertexMap.keys():
        U = vertexMap[v]
        mergedIndex2us[mergedVetexIndex] = U
        tmpMergeEdges = [edgeMap[(u, v)] for u in U]
        mergedEdge = mergeEdges(tmpMergeEdges, mergedVetexIndex, v)
        newEdges.append(mergedEdge[1:-3])  # 仅保留[dst]到 newEdges中进行后续编码,不保留 dst,starttime, endtiem, content，已经这几个要么已经编码了，要么不需要编码
        for u in U:
            if u not in u2mergedIndex.keys(): u2mergedIndex[u] = []
            u2mergedIndex[u].append(mergedVetexIndex)
        mergedIndex2content[mergedVetexIndex] = mergedEdge[-1]
        mergedVetexIndex += 1
    
    mapDict = {}   # {Field1:{Value: Index}, ...}  # dst, starttime, endtime
    mins = [sys.maxsize,sys.maxsize]  # minStartTime, minEndTime
    field = ['dst']
    data = newEdges
    for i in range(len(data)):
        tmpData = data[i]
        jsonObj = {}
        for j in range(len(field)):
            jsonObj[field[j]] = tmpData[j]
        mapDict = getFieldValueIndex_MappingDict(jsonObj=jsonObj, mapDict=mapDict, mins=mins)   
    
    with open('u2mergedIndex.pkl', 'wb') as file:
        pickle.dump(u2mergedIndex, file)
    with open('mergedIndex2us.pkl', 'wb') as file:
        pickle.dump(mergedIndex2us, file)
    with open('mapDict.pkl', 'wb') as file:
        pickle.dump(mapDict, file)
    with open('mergedIndex2content.pkl', 'wb') as file:
        pickle.dump(mergedIndex2content, file)

