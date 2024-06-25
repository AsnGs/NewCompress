# Environment-settings
**OS Version**:
[Ubuntu 22.04.3 LTS]

**Anaconda**:
conda 24.1.2

**GPU**: 
NVIDIA-SMI 535.171.04             Driver Version: 535.171.04   CUDA Version: 12.2 

**Python Libraries**:
[python==3.9, psycopg2, tqdm, scikit-learn==1.2.0, networkx==2.8.7, xxhash==3.2.0, graphviz==0.20.1
, pytorch==1.13.1, torchvision==0.14.1, torchaudio==0.13.1, pytorch-cuda=11.7, torch_geometric==2.0.0]

**Installing Commands**:
~~~
conda install psycopg2
conda install tqdm

pip install scikit-learn==1.2.0
pip install networkx==2.8.7
pip install xxhash==3.2.0
pip install graphviz==0.20.1

# PyTorch GPU version
conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.7 -c pytorch -c nvidia
pip install torch_geometric==2.0.0
pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-1.13.0+cu117.html
~~~
---