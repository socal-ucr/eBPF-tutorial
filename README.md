# eBPF-tutorial

## Step 1: Update System and Install Required Dependencies

To begin, update your system and install the required dependencies for eBPF, including `linux-tools-common`, `linux-tools-generic`, and the necessary kernel-specific tools `bpftool` is a utility that helps you manage and inspect eBPF programs. Install it by running the following commands:

### For Ubuntu/Debian-based systems:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y linux-tools-common linux-tools-generic linux-tools-$(uname -r)
```

### For CentOS/RHEL-based systems:
```bash
sudo yum update -y
sudo yum install -y linux-tools-common linux-tools-generic linux-tools-$(uname -r)
```
These tools allow you to compile, inspect, and manage eBPF programs.
If you encounter issues with installing bpftool via your package manager (especially for custom or cloud kernels), you can compile it manually from source. Follow the instructions in the bpftool GitHub repository to manually clone and build it.

## Step 2: Verify bpftool Installation

Once bpftool is installed, verify the installation by checking its version:

```bash
bpftool -V
```

You should see an output similar to:

```bash
bpftool v7.4.0
```

If you see this message, `bpftool` is correctly installed and ready to use.

## Step 3: Install bpftrace (Optional)

For advanced tracing of kernel events using eBPF, you can install `bpftrace`. This high-level tracing tool makes it easy to attach eBPF programs to tracepoints, function calls, and more.

### For Ubuntu/Debian-based systems:
```bash
sudo apt install bpfcc-tools bpftrace
```

### For CentOS/RHEL-based systems:
```bash
sudo yum install bpfcc-tools bpftrace
```

Once installed, you can use `bpftrace` to run dynamic tracing scripts. For example, to trace `execve` system calls, run:

```bash
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_execve { printf("execve syscall: %s\n", comm); }'
```

This will print the name of the program being executed each time the `execve` system call is made.

## Step 4: Install Docker

To set up Docker for the workloads, follow these steps:

### For Ubuntu/Debian-based Systems:
1. **Update the system**
  Update the system and install the required dependencies for Docker:
  
  ```bash
  sudo apt update
  sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
  ```

2. **Add Docker’s official GPG key:**

  ```bash
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
  ```

3. **Set up the Docker stable repository:**

  ```bash
  echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  ```

4. **Update the apt package list to include Docker:**

  ```bash
  sudo apt update
  ```

5. **Install Docker:**

  ```bash
  sudo apt install -y docker-ce
  ```

6. **Start Docker and verify that it's running:**

  ```bash
  sudo systemctl start docker
  sudo docker --version
  ```

  This will show the installed Docker version, confirming that Docker has been successfully installed.

## Step 5: Install Python 3.10 and Create Virtual Environment (Optional)

If you need Python 3.10 to set up a virtual environment, follow these steps:

### Install Python 3.10 and the venv package:

```bash
sudo apt install -y python3.10-venv
```

Once installed, you can create a virtual environment using the following command:

```bash
python3.10 -m venv myenv
```

Replace `myenv` with your desired virtual environment name.

Once these steps are complete, Docker will be ready for running containers, and Python 3.10 will be available for creating virtual environments.

## Step 6: Setting up the Docker Containers for Triton Server and Client

In this step, we will set up Docker containers for the Triton server and client, and configure the example model repository.

### 1. Run Triton Server in Docker

To begin, clone the `server` repository to get the example model repository and set it up.

```bash
git clone -b r25.08 https://github.com/triton-inference-server/server.git
cd server/docs/examples
```

### 2. Fetch the Models

Run the script to fetch the models:

```bash
./fetch_models.sh
```

### 3. Run Triton Server in Docker

Now, run the Triton server in a Docker container. Make sure that the model repository is correctly mapped to the container. Run the following command:

```bash
docker run -it --net=host --pid=host --name=triton-server -v ${PWD}/server/docs/examples/model_repository:/models nvcr.io/nvidia/tritonserver:25.08-py3 tritonserver --model-repository=/models
```

This will start the Triton server and load the models from the model_repository.

### 4. Verify Triton Server is Running

After starting the server, you should see logs in the terminal indicating that the Triton server has successfully started. The server should now be running and ready to serve the models.

### 5. Run Triton Client in Docker

To interact with the Triton server, you need the Triton client. Pull the Docker image for the Triton SDK:

```bash
docker pull nvcr.io/nvidia/tritonserver:25.08-py3-sdk
```

Once the image is pulled, run the Triton client in Docker:

```bash
docker run -it --net=host --pid=host --name=triton-client -v ${PWD}/server/docs/examples/model_repository:/models nvcr.io/nvidia/tritonserver:25.08-py3-sdk
```
This command will start the Triton client, and it will be able to interact with the server running on your system.

