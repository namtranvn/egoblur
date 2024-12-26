#!/bin/bash

# Install required packages
sudo dnf update -y
sudo dnf install -y curl docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Start and enable Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add NVIDIA repository
sudo dnf config-manager --add-repo https://nvidia.github.io/nvidia-docker/amzn2/nvidia-docker.repo

# Update package list
sudo dnf clean all
sudo dnf makecache

# Install NVIDIA driver and CUDA toolkit
sudo dnf -y install nvidia-driver nvidia-driver-cuda

# Install NVIDIA Container Toolkit
sudo dnf -y install nvidia-container-toolkit nvidia-docker2

# Configure Docker daemon
sudo nvidia-ctk runtime configure --runtime=docker

# Restart Docker daemon
sudo systemctl restart docker

# Verify NVIDIA driver installation
nvidia-smi

# Install CUDA toolkit if needed for development
sudo dnf -y install cuda-toolkit

# Restart Docker daemon
sudo systemctl restart docker