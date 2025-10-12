# eBPF Environment Setup Guide

## Update System and Install Required Dependencies

To begin, update your system and install the required dependencies for eBPF development. This includes `linux-tools-common`, `linux-tools-generic`, and the necessary kernel-specific tools. 

`bpftool` is a utility that helps you manage and inspect eBPF programs. Install it by running the following commands:

### For Ubuntu/Debian-based systems:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y linux-tools-common linux-tools-generic linux-tools-$(uname -r)
```

### Building bpftool from Source (if needed)

If the package installation doesn't work or you need the latest version, you can build `bpftool` from source:

```bash
cd ..
git clone --recurse-submodules https://github.com/libbpf/bpftool.git
cd bpftool/src 
make install 
```

Alternatively, pre-built `bpftool` binaries are available from [https://github.com/libbpf/bpftool/releases](https://github.com/libbpf/bpftool/releases).

## Step 2: Install BCC

BCC (BPF Compiler Collection) provides tools and libraries for working with eBPF. Please follow the installation guide in the [BCC GitHub repository](https://github.com/iovisor/bcc/blob/master/INSTALL.md).

## Step 3: Install bpftrace

For advanced tracing of kernel events using eBPF, you can install `bpftrace`. This high-level tracing tool makes it easy to attach eBPF programs to tracepoints, function calls, and more.

### For Ubuntu/Debian-based systems:
```bash
sudo apt install bpfcc-tools bpftrace
```
## Additional Dependencies

For the purposes of this tutorial, additional packages such as `pkg-config`, `libelf-dev`, `build-essential`, `clang`, and `file` are installed on the server as well.

## Install libbpf

`libbpf` is included as a submodule in this repository. You'll need to build and install it for the C-based examples to build correctly. See `libbpf/README.md` for more details.

