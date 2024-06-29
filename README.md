# Environment-settings
**OS Version**:
[Ubuntu 22.04.3 LTS]

**Anaconda**:
conda 24.1.2

**GPU**: 
NVIDIA-SMI 535.171.04             Driver Version: 535.171.04   CUDA Version: 12.2 

**Python Libraries**:
[python==3.9, psycopg2, tqdm, scikit-learn==1.2.0, networkx==2.8.7, xxhash==3.2.0, graphviz==0.20.1
, pytorch==1.13.1, torchvision==0.14.1, torchaudio==0.13.1, pytorch-cuda=11.7, torch_geometric==2.0.0, gdown=5.2.0]

**Installing Commands**:
~~~
conda install psycopg2
conda install tqdm

pip install scikit-learn==1.2.0
pip install networkx==2.8.7
pip install xxhash==3.2.0
pip install graphviz==0.20.1
pip install gdown==5.2.0

# PyTorch GPU version
conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.7 -c pytorch -c nvidia
pip install torch_geometric==2.0.0
pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-1.13.0+cu117.html
~~~
---
# Prepare Source Files
1.Download the JSON zip file corresponding to [E3 CADETS](https://drive.google.com/drive/folders/179uDuz62Aw61Ehft6MoJCpPeBEz16VFy) from Google Drive and unzip them.
~~~
gdown --fuzzy https://drive.google.com/file/d/1AcWrYiBmgAqp7DizclKJYYJJBQbnDMfb/view?usp=drive_link
gdown --fuzzy https://drive.google.com/file/d/1XLCEhf5DR8xw3S-Fimcj32IKnfzHFPJW/view?usp=drive_link
gdown --fuzzy https://drive.google.com/file/d/1EycO23tEvZVnN3VxOHZ7gdbSCwqEZTI1/view?usp=drive_link

find . -name "*.tar.gz" -print0 | xargs -0 -I {} tar -xzvf {}
~~~

2.Modify the _raw_dir_ variable in `config.py` to the location of the folder where the JSON files are located, and use `createData.py` to extract the required fields (Vertex: ['uuid', 'name', 'type'], Edge: ['src', 'dst', 'operation', 'timestamp']). The corresponding `vertex.csv` and `edge.csv` files are then created in the `artifact/csv`.
~~~
python creatData.py
~~~

3.Execute `structCompress.py` to compress the edges at the structual level and generate multiple mapping dicts to the `artifact/sc`.
~~~
python structCompress.py
~~~
