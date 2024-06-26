
from config import *
from utils import *



if __name__ == "__main__":
    print("-----Generate CSV from Raw Logs -----")

    os.makedirs(csv_dir, exist_ok=True)
    with open(os.path.join(csv_dir, vertex_csv_file), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['uuid', 'name', 'type'])
    with open(os.path.join(csv_dir, edge_csv_file), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['src', 'dst', 'operation', 'timestamp'])

    print("-----Processing Vertex-----")

    netobj2hash = store_netflow(file_path=raw_dir, csv_file=vertex_csv_file, filelist=filelist)
    file_obj2hash = store_file(file_path=raw_dir, csv_file=vertex_csv_file, filelist=filelist)
    subject_obj2hash = store_subject(file_path=raw_dir, csv_file=vertex_csv_file, filelist=filelist)

    print("-----Vertex CSV File Created-----\n")
    
    print("-----Processing Edges-----")

    minTime = store_event(
        file_path=raw_dir,
        reverse=edge_reversed,
        subject_uuid2hash=subject_obj2hash,
        file_uuid2hash=file_obj2hash,
        net_uuid2hash=netobj2hash,
        csv_file=edge_csv_file,
        filelist=filelist
    )
    with open(os.path.join('config.py'), mode='a+', newline='') as file:
        file.write('minsTime={}\n'.format(minTime))   
    print("-----Edge CSV File Created-----\n")



