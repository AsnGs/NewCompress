import os
import csv
import pickle
from config import *
from utils import *


def group_adjacent_numbers(nums):
    if not nums: return []
    groups = []
    start = nums[0]
    end = nums[0]
    for num in nums[1:]:
        if num == end + 1:end = num
        else:
            groups.append((start, end))
            start = num
            end = num
    groups.append((start, end))
    return groups

def contentCode(newEdges):
    processedData = []
    for edge in newEdges:
        tmpContent = []
        for key in edge[-1].keys():
            tmpContent.append(int(key)+2)
            for edgetype in edge[-1][key].keys():
                tmpContent.append(int(edgetype)+2)
                tmpContent.extend(group_adjacent_numbers([vertexOffset+2 for vertexOffset in edge[-1][key][edgetype]]))
                tmpContent.append(0)
            tmpContent.append(1)
        processedData.append(tmpContent)


# 嵌套字典
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

# 数组版本
# def consAndCodeContent(edgeList):
#     content = {}  # {timeOffset: [vertexOffset, type]} 

#     for i in range(len(edgeList)):
#         for j in range(len(edgeList[i])):
#             offsetTime = int(edgeList[i][j][1]) - minsTime #  offset
#             if offsetTime not in content.keys(): content[offsetTime] = []
#             content[offsetTime].append([i, rel2id[edgeList[i][j][0]]])
#     return content

# 本来是将单 u 的节点不合并不映射，放在外面处理了，但是考虑后还是将其统一了，同时也映射，算src部分的编码了
def mergeEdges(edgeList, mergedVetexIndex, v):
    mergedEdge = [mergedVetexIndex, v]  # [merged]
    times = [t - minsTime for t in sorted(list(set([int(e[1]) for edges in edgeList for e in edges])))]
    # startTime, endTime = min(times), max(times)
    if len(edgeList) == 1:
        mergedEdge.extend([times[0], times[0]])
    else:
        mergedEdge.extend([times[0], times[-1]])  

    specificContent = consAndCodeContent(edgeList)
    mergedEdge.append(specificContent)
    return mergedEdge

def getFieldValueIndex_MappingDict(jsonObj, mapDict):
    for i in range(len(jsonObj)):
        tempField = list(jsonObj.keys())[i]
        tempValue = jsonObj[tempField]
        if tempField == 'starttime' or tempField == 'endtime': # 时间跳过
            continue
        else:
            if tempField not in mapDict.keys():
                mapDict[tempField] = {}
            if tempValue not in mapDict[tempField].keys():
                mapDict[tempField][tempValue] = len(mapDict[tempField].keys())  # {field: {value: index}}
    return mapDict

# All vertex to its index
def createVertex2Index(csv_dir, vertex_csv_file):
    vertex2Index = {}  # Vertex to Index
    index2Vertex = {}  # Index to Vertex
    with open(os.path.join(csv_dir, vertex_csv_file), 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        vertexIndex = 0
        for vertex in reader:
            uuid = vertex[0]
            if not uuid in vertex2Index.keys():
                vertex2Index[uuid] = vertexIndex
                index2Vertex[vertexIndex] = uuid
                vertexIndex += 1
    return vertex2Index, index2Vertex

def createEdgeMap(csv_dir, edge_csv_file, vertex2Index):
    vertexMap = {} # vertexMap : {v:u}
    edgeMap = {} # edgeMap : {(u, v): e} 
    with open(os.path.join(csv_dir, edge_csv_file), 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
    
        for edge in reader:  # edge: [u,v, type, time]
            edge = [vertex2Index[edge[0]], vertex2Index[edge[1]], edge[2], edge[3]]
            if edge[1] not in vertexMap.keys():
                vertexMap[edge[1]] = [] 
            vertexMap[edge[1]].append(edge[0])
            if (edge[0], edge[1]) not in edgeMap.keys():  
                edgeMap[(edge[0], edge[1])] = []
            if edge[2:] not in edgeMap[(edge[0], edge[1])]:  # src,dst,type,time 完全相同就按一个算了
                edgeMap[(edge[0], edge[1])].append(edge[2:])
    return vertexMap, edgeMap

def createCompressStructMap(vertexMap, edgeMap):
    newEdges = [] # [mergedUIndex, vIndex, startTime, endTime, {timeOffset:{type:[vertexOffset]}}]
    mergedIndex2us = {}  # merged Vertex Index to u (one to many)  {i:[u1, u2, ...]}
    u2mergedIndex = {}  # vertex to merged Vertex Index (one to many) {u:[i1, i2, ...]}
    mergedIndex2content = {} # merged Vertex Index to its responding content {i1:conten1, ...]}

    mergedVetexIndex = 0
    for v in vertexMap.keys():
        U = vertexMap[v]
        mergedIndex2us[mergedVetexIndex] = U
        tmpMergeEdges = [edgeMap[(u, v)] for u in U]
        mergedEdge = mergeEdges(tmpMergeEdges, mergedVetexIndex, v)
        newEdges.append(mergedEdge)  
        for u in U:
            if u not in u2mergedIndex.keys(): 
                u2mergedIndex[u] = []
                u2mergedIndex[u].append(mergedVetexIndex)
            elif mergedVetexIndex not in u2mergedIndex[u]:
                u2mergedIndex[u].append(mergedVetexIndex)
        mergedIndex2content[mergedVetexIndex] = mergedEdge[-1]
        mergedVetexIndex += 1
    return u2mergedIndex, mergedIndex2us, mergedIndex2content, newEdges

if __name__ == '__main__':
    os.makedirs(sc_dir, exist_ok=True)

    id2char_dict = {}
    char2id_dict = {}
    
    #  Create vertex2Index Dict
    vertex2Index, index2Vertex = createVertex2Index(csv_dir=csv_dir, vertex_csv_file=vertex_csv_file)

    # Create Compressed Struct Dict
    vertexMap, edgeMap = createEdgeMap(csv_dir=csv_dir, edge_csv_file=edge_csv_file, vertex2Index=vertex2Index)    
    u2mergedIndex, mergedIndex2us, mergedIndex2content, newEdges = createCompressStructMap(vertexMap, edgeMap)
    
    with open('u2mergedIndex.pkl', 'wb') as file:
        pickle.dump(u2mergedIndex, file)
    with open('mergedIndex2us.pkl', 'wb') as file:
        pickle.dump(mergedIndex2us, file)
    with open('mergedIndex2content.pkl', 'wb') as file:
        pickle.dump(mergedIndex2content, file)

