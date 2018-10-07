#!/bin/bash
logger "W210: Downloading and installing NVIDIA CUDA"
wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.0.176-1_amd64.deb
wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64/libcudnn7_7.0.5.15-1+cuda9.0_amd64.deb
wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64/libcudnn7-dev_7.0.5.15-1+cuda9.0_amd64.deb
wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64/libnccl2_2.1.4-1+cuda9.0_amd64.deb
wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64/libnccl-dev_2.1.4-1+cuda9.0_amd64.deb
apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
dpkg -i cuda-repo-ubuntu1604_9.0.176-1_amd64.deb
dpkg -i libcudnn7_7.0.5.15-1+cuda9.0_amd64.deb
dpkg -i libcudnn7-dev_7.0.5.15-1+cuda9.0_amd64.deb
dpkg -i libnccl2_2.1.4-1+cuda9.0_amd64.deb
dpkg -i libnccl-dev_2.1.4-1+cuda9.0_amd64.deb
apt-get update
apt-get -y install cuda=9.0.176-1
apt-get install libcudnn7-dev
apt-get install libnccl-dev
logger "W210: Completed CUDA"
