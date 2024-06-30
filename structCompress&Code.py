import os
import csv
import json
import time
import logging
import numpy as np
from config import *
from utils import *


# Setting for logging
logger = logging.getLogger("structCompress&Code_logger")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_dir + 'structCompress&Code.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 将连续数字归组，offset 表示偏移量，delimiter 表示分隔符
def group_nodeOffset(n, delimiter):
    if not n: return []
    nums = [i for i in n]
    groups = ''
    start = nums[0]
    end = nums[0]
    for num in nums[1:]:
        if num == end + 1:end = num
        else:
            groups = groups + delimiter + str(start) + '-' + str(end)
            start = num
            end = num
    groups = groups + delimiter + str(start) + '-' + str(end)
    return groups


# edgeList: [[edgeType, time]]  -> content:{}
def consAndCodeContent(edgeList):
    content = {} # content: {offsetTime:{typeIndex:[vertexOffset]}}   # 多重字典嵌套
    for i in range(len(edgeList)):
        for j in range(len(edgeList[i])):
            offsetTime = int(edgeList[i][j][1]) - minsTime #  offset
            typeIndex = rel2id[edgeList[i][j][0]]
            if offsetTime not in content.keys(): content[offsetTime] = {}
            if typeIndex not in content[offsetTime].keys(): content[offsetTime][typeIndex] = []
            content[offsetTime][typeIndex].append(i)
    
    # 2作为 timeoffset 间的分隔符，1 作为 edgeType 之间的分隔符，0 作为nodeOffset 之间的分隔符
    tmpString = ''  # timeOffset+3  0 edgeTypeIndex+2 0  ' vertexOffset_1+2 - '
    for key in content.keys():
        tmpString += str(int(key)+3)
        for edgetype in content[key].keys():
            tmpString += '1'
            tmpString += str(int(edgetype)+3)
            tmpString += group_nodeOffset([vertexOffset+3 for vertexOffset in content[key][edgetype]], delimiter='0')
        tmpString += '2'  
    return tmpString

def mergeEdges(edgeList, mergedVetexIndex, v):
    mergedEdge = [mergedVetexIndex, v]  # [merged]
    times = [t - minsTime for t in sorted(list(set([int(e[1]) for edges in edgeList for e in edges])))]  # t - minsTime
    # startTime, endTime = min(times), max(times)
    if len(edgeList) == 1:
        mergedEdge.extend([times[0], times[0]])
    else:
        mergedEdge.extend([times[0], times[-1]])  

    mergedEdge.append(consAndCodeContent(edgeList))
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
def createVertex2Index(csv_dir, wholeMapDict):

    with open(os.path.join(csv_dir, vertex_csv_file), 'r') as csvfile:
        reader = csv.reader(csvfile)
        vertexData = list(reader)

    vertexField = vertexData[0]
    vertexData  = vertexData[1:]
    codedVertexData = []
    for data in vertexData:
        json_obj = {}
        for j in range(len(vertexField)):
            json_obj[vertexField[j]] = data[j]
        codedVertexData.append(codeVertex(json_obj, wholeMapDict, char2id_dict, id2char_dict))
    return wholeMapDict

def createEdgeMap(csv_dir, edge_csv_file, wholeMapDict):
    vertexMap = {} # vertexMap : {v:u}
    edgeMap = {} # edgeMap : {(u, v): e} 
    with open(os.path.join(csv_dir, edge_csv_file), 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        vertex2Index = wholeMapDict['uuid']
        for edge in reader:  # edge: [u,v, type, time]
            edge = [vertex2Index[edge[0]], vertex2Index[edge[1]], edge[2], edge[3]]
            if edge[1] not in vertexMap.keys():
                vertexMap[edge[1]] = [] 
            if edge[0] not in vertexMap[edge[1]]:
                vertexMap[edge[1]].append(edge[0])
            if (edge[0], edge[1]) not in edgeMap.keys():  
                edgeMap[(edge[0], edge[1])] = []
            if edge[2:] not in edgeMap[(edge[0], edge[1])]:  # src,dst,type,time 完全相同就按一个算了
                edgeMap[(edge[0], edge[1])].append(edge[2:])
    return vertexMap, edgeMap

def createCompressStructMap(vertexMap, edgeMap, wholeMapDict):
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
        # mergedIndex2content[mergedVetexIndex] = mergedEdge[-1]
        mergedVetexIndex += 1
    # return u2mergedIndex, mergedIndex2us, mergedIndex2content, newEdges
    wholeMapDict['u2mergedIndex'] = u2mergedIndex
    wholeMapDict['mergedIndex2us'] = mergedIndex2us

    return newEdges

def codeVertex(json_obj, wholeMapDict):
    codedDataList = []
    char2id_dict, id2char_dict = wholeMapDict['char2id_dict'], wholeMapDict['id2char_dict']
    for key in json_obj.keys():
        tmpValue = json_obj[key]
        if key not in wholeMapDict.keys(): wholeMapDict[key] = {}
        if str(tmpValue) not in wholeMapDict[key].keys():
            codedDataList.append(len(wholeMapDict[key].keys()))
            wholeMapDict[key][str(tmpValue)] = len(wholeMapDict[key].keys())
        else:
            codedDataList.append(wholeMapDict[key][str(tmpValue)])
    finalCodedData = list2char(codedDataList, char2id_dict, id2char_dict)
    return finalCodedData

def list2char(codedDataList, char2id_dict, id2char_dict):
    finalCodedData = []
    for value in codedDataList:
        tmpString = str(value)
        for char in tmpString:
            if char not in char2id_dict:
                end = len(char2id_dict) +2
                char2id_dict[char] = end
                id2char_dict[end] = char
                finalCodedData.append(end)
            else:
                finalCodedData.append(char2id_dict[char])
        finalCodedData.append(0)
    finalCodedData.append(1)
    return finalCodedData

if __name__ == '__main__':
    os.makedirs(sc_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    logger.info("Start logging of structCompree&Code.")

    wholeMapDict= {}
    wholeMapDict['id2char_dict'] = {}
    wholeMapDict['char2id_dict'] = {}
    
    with open(os.path.join(csv_dir, vertex_csv_file), 'r') as csvfile:
        reader = csv.reader(csvfile)
        vertexData = list(reader)

    start_time = time.time()
    vertexField = vertexData[0]
    vertexData  = vertexData[1:]
    codedVertexData = []
    for data in vertexData:
        json_obj = {}
        for j in range(len(vertexField)):
            json_obj[vertexField[j]] = data[j]
        codedVertexData.append(codeVertex(json_obj, wholeMapDict))
    codedVertexArray = np.array([c for item in codedVertexData for c in item]) # processed vertex data -> flatten
    codedVertexArray = codedVertexArray.reshape(len(codedVertexArray), 1)
    np.save(os.path.join(sc_dir, codedVertexNPYFile), codedVertexArray)
    end_time = time.time()
    logger.info(f'The time of mapping and coding vertexes is : {(end_time - start_time)} seconds.')

    start_time = time.time()
    # Create Compressed Struct Dict
    vertexMap, edgeMap = createEdgeMap(csv_dir=csv_dir, edge_csv_file=edge_csv_file, wholeMapDict=wholeMapDict)    
    newEdges = createCompressStructMap(vertexMap, edgeMap, wholeMapDict)

    codedEdgeData = []
    for data in newEdges:
        codedEdgeData.append(list2char(data, wholeMapDict['char2id_dict'], wholeMapDict['id2char_dict']))
    codedEdgeArray = np.array([c for item in codedEdgeData for c in item])
    codedEdgeArray = codedEdgeArray.reshape(len(codedEdgeArray), 1)
    np.save(os.path.join(sc_dir, codedEdgeNPYFile), codedEdgeArray) 
    end_time = time.time()   
    logger.info(f'The time of compressing and coding edges is : {(end_time - start_time)} seconds')
                
    with open(os.path.join(sc_dir, wholeMapDictFile), mode='w') as f:
        json.dump(wholeMapDict, f, indent=4)

