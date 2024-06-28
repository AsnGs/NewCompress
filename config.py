########################################################
#
#                   Artifacts path
#
########################################################

# The directory of the raw logs
raw_dir = '/home/yingjie/Darpa/E3-Cadets/'

# The directory to save all artifacts
artifact_dir = './artifact/'

csv_dir = artifact_dir + "csv"
sc_dir = artifact_dir + "sc"   # structure compressed

vertex_csv_file = 'vertex.csv'
edge_csv_file = 'edge.csv'
structMap_json_file = 'structMap.json'
mapping_json_file = 'mapping.json'


########################################################
#
#               Graph semantics
#
########################################################

# The directions of the following edge types need to be reversed
edge_reversed = [
    "EVENT_RECVFROM",
    "EVENT_READ"
]

include_edge_type=[
    'EVENT_READ',
    'EVENT_WRITE',
    'EVENT_EXECUTE',
    'EVENT_RECVFROM',
    'EVENT_SENDTO',
    'EVENT_SENDMSG',
    'EVENT_FORK',
    'EVENT_CLONE'
]

relMap = {
 'EVENT_WRITE': 'EVENT_WRITE',
 'EVENT_READ' : 'EVENT_READ',
 'EVENT_EXECUTE': 'EVENT_EXECUTE',
 'EVENT_SENDTO': 'EVENT_WRITE',
 'EVENT_SENDMSG': 'EVENT_WRITE',
 'EVENT_RECVFROM': 'EVENT_READ',
 'EVENT_FORK': 'EVENT_FORK',
 'EVENT_CLONE': 'EVENT_FORK',
}

rel2id = {
 1: 'EVENT_WRITE',
 'EVENT_WRITE': 1,
 2: 'EVENT_READ',
 'EVENT_READ': 2,
 3: 'EVENT_EXECUTE',
 'EVENT_EXECUTE': 3,
 4: 'EVENT_FORK',
 'EVENT_FORK': 4,
}


########################################################
#
#               Raw Data Json Files
#
########################################################

# filelist = ['ta1-cadets-e3-official.json',
#  'ta1-cadets-e3-official.json.1',
#  'ta1-cadets-e3-official.json.2',
#  'ta1-cadets-e3-official-1.json',
#  'ta1-cadets-e3-official-1.json.1',
#  'ta1-cadets-e3-official-1.json.2',
#  'ta1-cadets-e3-official-1.json.3',
#  'ta1-cadets-e3-official-1.json.4',
#  'ta1-cadets-e3-official-2.json',
#  'ta1-cadets-e3-official-2.json.1']

filelist = ['ta1-cadets-e3-official.json',
 'ta1-cadets-e3-official.json.1',
 'ta1-cadets-e3-official.json.2',]

minsTime=1522706863
minsTime=1522706863
