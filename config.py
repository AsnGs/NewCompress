########################################################
#
#                   Artifacts path
#
########################################################

# The directory of the raw logs
raw_dir = '/home/yingjie/Darpa/E3-Cadets/'

# The directory to save all artifacts
artifact_dir = './artifact/'

csv_dir = artifact_dir + "csvs"

vertex_csv_file = 'vertex.csv'
edge_csv_file = 'edge.csv'

########################################################
#
#               Graph semantics
#
########################################################

# The directions of the following edge types need to be reversed
edge_reversed = [
    "EVENT_RECVFROM",
    "EVENT_RECVMSG",
    "EVENT_READ",
    'EVENT_MMAP',
    'EVENT_EXECUTE'
]