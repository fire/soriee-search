# Soriee Search

The code is a set of commands for setting up and running a search application called "Soriee Search". It involves installing CUDA, NVIDIA container toolkit, Docker, and other dependencies. The application uses a pre-built Docker image called "marqoai/marqo:latest" to run a Python script that performs text and image searches. The code also includes a command to load photos from a specific GitHub repository using a local HTTP server.

# Marqo

```bash
bash
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/12.0.0/local_installers/cuda-repo-wsl-ubuntu-12-0-local_12.0.0-1_amd64.deb
sudo dpkg -i cuda-repo-wsl-ubuntu-12-0-local_12.0.0-1_amd64.deb
sudo cp /var/cuda-repo-wsl-ubuntu-12-0-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
      && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
            sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
            sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo apt-get update && sudo apt-get install docker-compose-plugin
sudo usermod -aG docker $USER
sudo update-alternatives --set iptables /usr/sbin/iptables-legacy
sudo update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy
sudo service docker start
```

```bat
docker rm -f marqo
docker pull marqoai/marqo:latest
docker run --name marqo --gpus all -it --privileged -p 8882:8882 --add-host host.docker.internal:host-gateway marqoai/marqo:latest
docker log --follow marqo
micromamba run -n base python .\first-index.py
micromamba run -n base python .\first-search.py
micromamba run -n base pip install streamlit
micromamba run -n base streamlit run text-image-search.py
```

```bat
# load photos from https://github.com/alexeygrigorev/clothing-dataset
python3 -m http.server 8222
```