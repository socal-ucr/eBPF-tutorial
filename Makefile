# Define variables
DOCKER_IMAGE_TAG=25.08-py3
TRITON_REPO=https://github.com/triton-inference-server/server.git
MODEL_REPO_PATH=${PWD}/server/docs/examples/model_repository

# Update system and install necessary packages
update_system:
	sudo apt update && sudo apt upgrade -y
	sudo apt install -y linux-tools-common linux-tools-generic linux-tools-$(uname -r)
	bpftool -V

# Install Docker
install_docker:
	sudo apt update
	sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
	echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
	sudo apt update
	sudo apt install -y docker-ce
	sudo systemctl start docker
	sudo docker --version

# Install Python3.10 and create venv
install_python_venv:
	sudo apt install -y python3.10-venv
	gnome-terminal -- bash -c "echo 'Python3.10 venv installed. Press Enter to continue...'; exec bash"

# Run Triton server
run_triton_server:
	git clone -b r25.08 $(TRITON_REPO)
	cd server/docs/examples && ./fetch_models.sh
	docker run -it --net=host --pid=host --name=triton-server -v ${PWD}/server/docs/examples/model_repository:/models nvcr.io/nvidia/tritonserver:$(DOCKER_IMAGE_TAG) tritonserver --model-repository=/models
	gnome-terminal -- bash -c "echo 'Server created. Press Enter to continue...'; exec bash"

# Run Triton client
run_triton_client:
	docker pull nvcr.io/nvidia/tritonserver:$(DOCKER_IMAGE_TAG)-sdk
	docker run -it --net=host --pid=host --name=triton-client -v ${PWD}/server/docs/examples/model_repository:/models nvcr.io/nvidia/tritonserver:$(DOCKER_IMAGE_TAG)-sdk

# Default target to execute all steps
all: update_system install_docker install_python_venv run_triton_server run_triton_client
