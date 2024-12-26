# Add NVIDIA package repositories
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
    && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo rpm --import - \
    && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.repo | sudo tee /etc/yum.repos.d/nvidia-docker.repo

# Install required packages
sudo yum install -y epel-release
sudo yum clean expire-cache

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