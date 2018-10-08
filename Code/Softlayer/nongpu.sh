#!/bin/bash


logger "W210: Starting base installation"
apt-get update

# Python Installation
logger "W210: Installing python pip"
apt-get -y install python3-pip
pip3 install --upgrade pip

# TensorFlow
logger "W210: Installing Tensorflow"
python3 -m pip install --upgrade tensorflow

# Indico FineTune
logger "W210: Installing FineTune"
apt-get -y install libjpeg8-dev zlib1g-dev
python3 -m pip install --upgrade finetune
logger "W210: Completed FineTune"

# Jupyterlab
logger "W210: Installing JupyterLabs"
python3 -m pip install --upgrade jupyterlab

# GIT
logger "W210: Installing git and pulling in code"
apt-get -y install git
cd /
git clone https://github.com/pdurkin84/W210_Gov_Complaints_Portal

# install test tool for tensorflow
cd /root
git clone https://github.com/tensorflow/models.git
echo "Test tensorflow install with\npython models/tutorials/image/mnist/convolutional.py\nshows 200ms per-step with no GPU" >> /root/testTF.md
logger "W210: Completed"
logger "W210: Installation completed, still need to run: /W210_Gov_Complaints_Portal/Code/Softlayer/install_iptables.sh"
