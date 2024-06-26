import os
import csv
from config import *
from utils import *

def getFieldValueIndex_MappingDict(jsonObj, mapDict, mins):
    for i in range(len(jsonObj)):
        tempField = list(jsonObj.keys())[i]
        tempValue = jsonObj[tempField]
        if tempField == 'timestamp':
            if int(tempValue) <= mins[0]:
                mins[0] = int(tempValue)
        elif tempField == 'src' or tempField == 'dst':
            continue
        else:
            if tempField not in mapDict.keys():
                mapDict[tempField] = {}
            if tempValue not in mapDict[tempField].keys():
                mapDict[tempField][tempValue] = len(mapDict[tempField].keys())  # {field: {value: index}}
    return mapDict
    

if __name__ == '__main__':
    os.makedirs(sc_dir, exist_ok=True)
    mapDict = {}   # {Field1:{Value: Index}, ...}
    mins = [sys.maxsize]

    print("-----Start  Mapping  Vertex-----")
    with open(os.path.join(csv_dir, vertex_csv_file), 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
    field = data[0]
    data  = data[1:]
    
    for i in range(len(data)):
        tmpData = data[i]
        jsonObj = {}
        for j in range(len(field)):
            jsonObj[field[j]] = tmpData[j]
        mapDict = getFieldValueIndex_MappingDict(jsonObj=jsonObj, mapDict=mapDict, mins=mins)
    print("-----Mapping Vertex  End------")

    mapDict['operation'] = rel2id
        

    print("-----Start   Mapping Edge-----")
    with open(os.path.join(csv_dir, edge_csv_file), 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
    field = data[0]
    data  = data[1:]
    
    for i in range(len(data)):
        tmpData = data[i]
        jsonObj = {}
        for j in range(len(field)):
            jsonObj[field[j]] = tmpData[j]
        mapDict = getFieldValueIndex_MappingDict(jsonObj=jsonObj, mapDict=mapDict, mins=mins)
    print("-----Mapping Edge    End------")
    
    
