curl -X 'POST' \
  'http://localhost:8000/v1/blur' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "input_video_path": "test_video.mp4",
  "face_model_score_threshold": 0.9,
  "lp_model_score_threshold": 0.9,
  "nms_iou_threshold": 0.3,
  "scale_factor_detections": 1,
  "output_video_fps": 30
}'

If you're experiencing issues with NVIDIA drivers on an EC2 G5 instance running Ubuntu 22.04 where `nvidia-smi` is failing due to communication problems, here's how to fix it:

First, let's install the correct NVIDIA drivers using the AWS-recommended method:

```bash
# Update package lists
sudo apt update

# Install necessary dependencies
sudo apt install -y build-essential gcc make linux-headers-$(uname -r)

# Add the NVIDIA repository
sudo add-apt-repository -y ppa:graphics-drivers/ppa
sudo apt update

# Install the NVIDIA driver specifically for G5 instances (which use NVIDIA A10G GPUs)
sudo apt install -y nvidia-driver-525-server nvidia-utils-525-server

# Remove any conflicting nouveau drivers
sudo bash -c "echo blacklist nouveau > /etc/modprobe.d/blacklist-nouveau.conf"
sudo bash -c "echo options nouveau modeset=0 >> /etc/modprobe.d/blacklist-nouveau.conf"
sudo update-initramfs -u

# Reboot the instance to apply changes
sudo reboot
```

After your instance reboots, try running `nvidia-smi` again. This should resolve the communication issue.

If you're still having problems, you can try the direct installation method using NVIDIA's installer:

```bash
# Download the appropriate driver (525.85.12 works well with G5 instances)
wget https://us.download.nvidia.com/tesla/525.85.12/NVIDIA-Linux-x86_64-525.85.12.run

# Make it executable
chmod +x NVIDIA-Linux-x86_64-525.85.12.run

# Install the driver
sudo ./NVIDIA-Linux-x86_64-525.85.12.run --silent --dkms

# Reboot again
sudo reboot
```

After following either of these methods, the NVIDIA driver should be properly installed and `nvidia-smi` should work correctly.
