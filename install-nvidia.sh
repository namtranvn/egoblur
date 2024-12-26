#!/bin/bash

# Exit on error
set -e

# # Install required packages
# sudo dnf update -y
# sudo dnf install -y curl docker

# # Install Docker Compose
# sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
# sudo chmod +x /usr/local/bin/docker-compose

# # Start and enable Docker service
# sudo systemctl start docker
# sudo systemctl enable docker

echo "Installing required packages..."
sudo dnf update -y
sudo dnf install -y gcc kernel-devel-$(uname -r) kernel-headers-$(uname -r)

echo "Installing NVIDIA driver..."
sudo dnf config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/rhel9/x86_64/cuda-rhel9.repo
sudo dnf clean all
sudo dnf module install -y nvidia-driver:latest-dkms

echo "Installing CUDA toolkit..."
sudo dnf install -y cuda-toolkit

echo "Installing Docker..."
sudo dnf install -y docker

echo "Installing NVIDIA Container Toolkit..."
sudo dnf config-manager --add-repo https://nvidia.github.io/libnvidia-container/stable/rpm/nvidia-container-toolkit.repo
sudo dnf install -y nvidia-container-toolkit

echo "Configuring Docker daemon..."
sudo nvidia-ctk runtime configure --runtime=docker

echo "Starting Docker service..."
sudo systemctl start docker
sudo systemctl enable docker

echo "Restarting Docker daemon..."
sudo systemctl restart docker

echo "Verifying NVIDIA driver installation..."
nvidia-smi

echo "Installation complete! System will reboot in 10 seconds..."
sleep 10
sudo reboot