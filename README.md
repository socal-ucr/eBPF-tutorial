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
