#!/bin/bash
set -e

echo "Uninstalling any old versions..."
sudo apt-get remove -y docker docker-engine docker.io containerd runc || true

echo "Updating package list..."
sudo apt-get update

echo "Installing prerequisites..."
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

echo "Adding Docker's official GPG key..."
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo "Setting up Docker repository..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "Updating package list with Docker repository..."
sudo apt-get update

echo "Installing Docker Engine..."
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

echo "Adding current user to docker group..."
sudo usermod -aG docker $USER

echo "Installing Docker Compose..."
sudo apt-get install -y docker-compose-plugin

echo "Verifying Docker installation..."
docker --version

echo "Verifying Docker Compose installation..."
docker compose version

echo "Starting Docker service..."
sudo systemctl start docker
sudo systemctl enable docker

# Add NVIDIA package repositories
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
   && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

# Install nvidia-docker2
sudo apt-get update
sudo apt-get install -y nvidia-docker2

#
sudo apt-get update
sudo apt-get install -y nvidia-cuda-toolkit

#
nvidia-smi 

# Install NVIDIA Container Toolkit
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# Configure Docker daemon
sudo nvidia-ctk runtime configure --runtime=docker

# Restart Docker daemon
sudo systemctl restart docker