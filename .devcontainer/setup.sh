#!/bin/bash
# ---------------------------------------------------------
# inzva Week 11 - Codespace Post-Create Setup
# This script runs automatically when the Codespace is created.
# Only installs OS-level tools. Students install uv themselves!
# ---------------------------------------------------------

set -e

echo "Setting up inzva Week 11 environment..."

# -- Install htop + openssh-client (Module 1) --
echo "Installing htop and openssh-client..."
sudo apt-get update -qq && sudo apt-get install -y -qq htop openssh-client > /dev/null 2>&1

# -- Wait for Docker daemon to be ready --
echo "Waiting for Docker daemon..."
for i in $(seq 1 30); do
  if docker info > /dev/null 2>&1; then
    echo "Docker is ready!"
    break
  fi
  if [ "$i" -eq 30 ]; then
    echo "WARNING: Docker daemon not available after 30s - SSH server skipped."
    echo "  Run manually: docker build -t inzva-ssh-server ./ssh-server && docker run -d --name ssh-demo -p 2222:22 inzva-ssh-server"
    exit 0
  fi
  sleep 1
done

# -- Build and start the SSH demo server (Module 1, SSH exercise) --
echo "Building SSH demo server..."
docker build -t inzva-ssh-server ./ssh-server > /dev/null 2>&1
echo "Starting SSH demo server on port 2222..."
docker run -d --name ssh-demo -p 2222:22 inzva-ssh-server > /dev/null 2>&1

echo ""
echo "======================================================"
echo "  Codespace is ready!"
echo ""
echo "  Pre-installed:"
echo "    - Python 3.11    - Docker & Docker Compose"
echo "    - htop           - git"
echo "    - SSH demo server running on port 2222"
echo ""
echo "  Open index.html for the lab manual"
echo ""
echo "  First task: install uv (Module 1, Step 8)"
echo "  -> curl -LsSf https://astral.sh/uv/install.sh | sh"
echo "======================================================"
echo ""
