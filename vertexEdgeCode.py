import os
import csv
import pickle
import numpy as np
from config import *
from utils import *

def createMappingDict(field, data, mappingDict):
    for i in range(len(data)):
        tempData  = data[i]
        for j in range(len(field)):
            tempFiled = field[j]
            if tempFiled == 'timestamp':
                if int(tempData[j]) <= minTime:
                    minTime = int(tempData[j])
            elif tempFiled == 'src' or tempFiled == 'dst' or tempFiled == 'uuid':
                continue
            else:
                if tempFiled not in mappingDict.keys():
                    mappingDict[tempFiled] = {}
                if str(tempData[j]) not in mappingDict[tempFiled].keys():
                    mappingDict[tempFiled][str(tempData[j])] = len(mappingDict[tempFiled].keys())
    return mappingDict  

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



def codeVertex(json_obj, vertexMappingDict, char2id_dict, id2char_dict):
    codedDataList = []
    for key in json_obj.keys():
        tmpValue = json_obj[key]
        if key == 'uuid':
            codedDataList.append(vertexMappingDict['uuid'][json_obj[key]])
        else:
            if key not in vertexMappingDict.keys(): vertexMappingDict[key] = {}
            if str(tmpValue) not in vertexMappingDict[key].keys():
                codedDataList.append(len(vertexMappingDict[key].keys()))
                vertexMappingDict[key][str(tmpValue)] = len(vertexMappingDict[key].keys())
            else:
                codedDataList.append(vertexMappingDict[key][str(tmpValue)])
    finalCodedData = list2char(codedDataList, char2id_dict, id2char_dict)
    return finalCodedData


if __name__ == '__main__':
    
    id2char_dict = {}
    char2id_dict = {}

    vertexMappingDict = {}
    with open(os.path.join(sc_dir, vertex2IndexFile), 'rb') as f:
        vertex2Index = pickle.load(f)
    vertexMappingDict['uuid'] = vertex2Index
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
        codedVertexData.append(codeVertex(json_obj, vertexMappingDict, char2id_dict, id2char_dict))
    codedVertexArray = np.array([c for item in codedVertexData for c in item]) # processed vertex data -> flatten
    codedVertexArray = codedVertexArray.reshape(len(codedVertexArray), 1)
    np.save(os.path.join(sc_dir, codedVertexNPYFile), codedVertexArray)


    # newEdges
    codedEdgeData = []
    with open(os.path.join(sc_dir, 'newEdges.pkl'), 'rb') as f:
        newEdges = pickle.load(f)
    for data in newEdges:
        codedEdgeData.append(list2char(data, char2id_dict, id2char_dict))
    codedEdgeArray = np.array([c for item in codedEdgeData for c in item])
    codedEdgeArray = codedEdgeArray.reshape(len(codedEdgeArray), 1)
    np.save(os.path.join(sc_dir, codedEdgeNPYFile), codedEdgeArray)


