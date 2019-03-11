set -e -x

# https://docs.docker.com/install/linux/docker-ce/ubuntu/#set-up-the-repository
apt-get update
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
apt-key fingerprint 0EBFCD88
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
apt-get update
apt-get install -y docker-ce

# https://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo
sudo gpasswd -a $USER docker

wget https://github.com/docker/compose/releases/download/1.23.2/docker-compose-Linux-x86_64 -O /usr/bin/docker-compose
chmod a+x /usr/bin/docker-compose

docker --version
docker-compose --version
