#!/bin/bash
set -e

# echo "Uninstalling any old versions..."
# sudo apt-get remove -y docker docker-engine docker.io containerd runc || true

# echo "Updating package list..."
# sudo apt-get update

# echo "Installing prerequisites..."
# sudo apt-get install -y \
#     ca-certificates \
#     curl \
#     gnupg \
#     lsb-release

# echo "Adding Docker's official GPG key..."
# sudo mkdir -p /etc/apt/keyrings
# curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# echo "Setting up Docker repository..."
# echo \
#   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
#   $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# echo "Updating package list with Docker repository..."
# sudo apt-get update

# echo "Installing Docker Engine..."
# sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# echo "Adding current user to docker group..."
# sudo usermod -aG docker $USER

# echo "Installing Docker Compose..."
# sudo apt-get install -y docker-compose-plugin

# echo "Verifying Docker installation..."
# docker --version

# echo "Verifying Docker Compose installation..."
# docker compose version

# echo "Starting Docker service..."
# sudo systemctl start docker
# sudo systemctl enable docker

echo "Installing curl and wget..."
sudo apt-get update
sudo apt-get install -y curl wget

echo "Installing NVIDIA Container Toolkit..."
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

echo "Updating package list..."
sudo apt-get update

echo "Installing nvidia-container-toolkit..."
sudo apt-get install -y nvidia-container-toolkit

echo "Configuring Docker..."
sudo nvidia-ctk runtime configure --runtime=docker

echo "Restarting Docker daemon..."
sudo systemctl restart docker

echo "Testing NVIDIA Docker installation..."
sudo docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi

echo "Installation complete!"