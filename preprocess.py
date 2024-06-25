import os
import sys
import csv
from tqdm import tqdm
import hashlib

from config import *

def createMappingDict(field, data, mappingDict):
    for i in range(len(data)):
        tempData  = data[i]
        for j in range(len(field)):
            tempFiled = field[j]
            if tempFiled == 'timestamp':
                if int(tempData[j]) <= minTime:
                    minTime = int(tempData[j])
            elif tempFiled == 'src' or tempFiled == 'dst':
                continue
            else:
                if tempFiled not in mappingDict.keys():
                    mappingDict[tempFiled] = {}
                if str(tempData[j]) not in mappingDict[tempFiled].keys():
                    mappingDict[tempFiled][str(tempData[j])] = len(mappingDict[tempFiled].keys())
    return mappingDict    
        
        


if __name__ == '__main__':
    edges = []   # 保留边
    vertexData = []
    vertexField = []
    mappingDict = {}
    minTime = sys.maxsize

    with open(os.path.join(csv_dir, vertex_csv_file), 'r') as csvfile:
        reader = csv.reader(csvfile)
        vertexData = list(reader)

    vertexField = vertexData[0]
    vertexData  = vertexData[1:]

    mappingDict = createMappingDict(vertexField, vertexData, mappingDict)

    with open(os.path.join(csv_dir, edge_csv_file), 'r') as csvfile:
        reader = csv.reader(csvfile)
        edgeData = list(reader)

    edgeField = edgeData[0]
    edgeData  = edgeData[1:]

    mappingDict = createMappingDict(edgeField, edgeData, mappingDict)

    pass


    
        
