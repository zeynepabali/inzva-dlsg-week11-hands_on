#!/bin/bash
# Setup: runs once when the Codespace is first created
set -e
echo "[setup] Installing htop and openssh-client..."
sudo apt-get update -qq && sudo apt-get install -y -qq htop openssh-client > /dev/null 2>&1
echo "[setup] Done."
