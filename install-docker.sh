#!/bin/bash
set -e

sudo apt-get remove -y docker docker-engine docker.io containerd runc || true

sudo apt-get update

sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

sudo usermod -aG docker $USER

sudo apt-get install -y docker-compose-plugin

docker --version

docker compose version

sudo systemctl start docker
sudo systemctl enable docker

sudo chown root:docker /var/run/docker.sock
sudo chmod 666 /var/run/docker.sock

sudo systemctl restart docker