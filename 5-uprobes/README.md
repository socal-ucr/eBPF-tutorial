# eBPF Uprobe: Tracing gRPC Function Calls in Triton

This example demonstrates how to use **eBPF uprobes** to trace a **user-space function** inside the **Triton Inference Server binary**.  
Specifically, it hooks into the gRPC function  
`grpc_chttp2_maybe_complete_recv_trailing_metadata()`  
to print a message every time it is called.

Unlike kprobes (which trace kernel syscalls), **uprobes** trace functions in **user-space applications** such as Triton or other binaries.

---

## What this example does

- Finds the **PID** of a running Docker container by name.
- Loads a small **eBPF uprobe program** that attaches to a specific function in the Triton binary.
- Prints a message every time the `grpc_chttp2_maybe_complete_recv_trailing_metadata()` function is executed.
- Uses `bpf_trace_printk()` to log messages directly from the BPF program.


## Locate the Triton binary inside Docker’s overlay2

For hooking user space probes we need to find the triton binary file. The binary files of the docker containers are generally located inside the `overlay2` directory. To locate the `overlay2` directory run the following command:
```bash
docker info | grep "Docker Root Dir"
# Example: /var/lib/docker/
```

Using the following command, find the specific binary file for the `tritonserver`:
```bash
find /var/lib/docker/overlay2/ -type f -name "tritonserver"
```
    
```bash
# Example result:
/var/lib/docker/overlay2/6f3e90...dd0f/diff/opt/tritonserver/bin/tritonserver
```

## Look for the function symbol in the target binary

This shows all the symbols for a specific function.
```bash
sudo objdump -t <tritonserver-binary-path> | grep <function-name>​
```

This command demangles the function symbol to match it with the actual function signature:
```bash
echo <symbol> | c++filt
```

## How to Run
Run as root or with sudo privileges
```bash
sudo python3 uprobe.py -c <container_name>
```
Replace `<container_name>` with the name of your Triton container (e.g., tritonserver).