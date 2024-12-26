#!/bin/bash
# Determine CentOS version
CENTOS_VERSION=$(cat /etc/centos-release | tr -dc '0-9.' | cut -d \. -f1)

# Install EPEL based on CentOS version
if [ "$CENTOS_VERSION" = "7" ]; then
    sudo yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
elif [ "$CENTOS_VERSION" = "8" ]; then
    sudo dnf install -y epel-release epel-next-release
elif [ "$CENTOS_VERSION" = "9" ]; then
    sudo dnf install -y epel-release epel-next-release
else
    echo "Unsupported CentOS version: $CENTOS_VERSION"
    exit 1
fi

# Add NVIDIA package repositories
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
    && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo rpm --import - \
    && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.repo | sudo tee /etc/yum.repos.d/nvidia-docker.repo

# Clean and update package cache
sudo yum clean expire-cache
sudo yum check-update

# Install nvidia-docker2
sudo yum install -y nvidia-docker2

# Install NVIDIA CUDA toolkit
sudo yum install -y nvidia-cuda-toolkit

# Verify NVIDIA drivers are working
nvidia-smi

# Install NVIDIA Container Toolkit
sudo yum install -y nvidia-container-toolkit

# Configure Docker daemon
sudo nvidia-ctk runtime configure --runtime=docker

# Restart Docker daemon
sudo systemctl restart docker