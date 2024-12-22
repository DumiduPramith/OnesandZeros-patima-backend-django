#!/bin/bash

# Update package list
sudo apt-get update && sudo apt-get install -y ca-certificates curl || { echo "Failed to install dependencies"; exit 1; }

# Create directory for apt keyrings
sudo install -m 0755 -d /etc/apt/keyrings || { echo "Failed to create /etc/apt/keyrings"; exit 1; }

# Download and add Docker GPG key
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc || { echo "Failed to download Docker GPG key"; exit 1; }
sudo chmod a+r /etc/apt/keyrings/docker.asc || { echo "Failed to set permissions for Docker GPG key"; exit 1; }

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null || { echo "Failed to add Docker repository"; exit 1; }

# Update package list and install Docker
sudo apt-get update && sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin || { echo "Failed to install Docker"; exit 1; }

# Create Docker group and add the current user
sudo groupadd -f docker || { echo "Failed to create Docker group"; exit 1; }
sudo usermod -aG docker $USER || { echo "Failed to add user to Docker group"; exit 1; }

# Install Git LFS
sudo apt-get install -y git-lfs || { echo "Failed to install Git LFS"; exit 1; }

# Display a message for the user
echo "Docker and Git LFS have been installed successfully. Please log out and log back in to use Docker without sudo."
git lfs install
git lfs pull