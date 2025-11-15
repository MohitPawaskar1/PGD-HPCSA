# update
sudo apt update && sudo apt upgrade -y

# install basics
sudo apt install -y git curl apt-transport-https conntrack

# docker (if not installed)
# follow Docker official; quick install:
sudo apt install -y docker.io
sudo usermod -aG docker $USER
newgrp docker

# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl && sudo mv kubectl /usr/local/bin/

# minikube (recommended for local)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# helm (for prometheus/grafana)
#!/bin/bash

PYTHON_VERSION="3.12"

sudo apt update

# Do NOT remove base python3 package or dependencies

# Optionally remove non-base Python versions installed outside apt:
# (You may customize this if you installed other versions via deadsnakes PPA, pyenv, or manually.)

# Install desired Python version and essential packages via apt
sudo apt install -y python${PYTHON_VERSION} python${PYTHON_VERSION}-venv python${PYTHON_VERSION}-dev python3-ipykernel jupyter-notebook

# Configure global python3 alternative
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION} 1
sudo update-alternatives --set python3 /usr/bin/python${PYTHON_VERSION}

# Register ipykernel for the chosen Python
python3 -m ipykernel install --user --name=python3 --display-name="Python 3 (Default)"

# Remove extra Jupyter kernels safely (only if jupyter command exists)
if command -v jupyter &> /dev/null; then
  jupyter kernelspec list | grep -v 'python3' | awk '{print $1}' | while read -r kernel; do
    jupyter kernelspec uninstall -y "$kernel"
  done
fi

echo "Python $PYTHON_VERSION is set as global default with Jupyter kernel configured."
echo "Please open Jupyter notebooks; it should no longer ask for kernel selection."

curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
