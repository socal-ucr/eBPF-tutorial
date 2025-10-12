# Minimal eBPF Kprobe: Print with `bpf_trace_printk`

This example shows the smallest possible **BCC/eBPF kprobe** for tracing a single syscall (`recvfrom`) made by a specific Docker container (Triton).  
It prints directly from the BPF program using `bpf_trace_printk`.

---

## What this example does

- Finds the **PID** of a Docker container by name.  
- Loads a tiny eBPF program that:
  - Filters events to that PID only.  
  - Hooks into `__x64_sys_recvfrom`.  
  - Prints `pid`, `fd`, and `comm` (process name) via `bpf_trace_printk`.  
- Streams kernel trace output to your terminal with `b.trace_print()`.

---

## How to run

```bash
# Run as root/sudo because tracing needs elevated privileges
sudo python3 kprobe.py -c <triton_container_name>
```
Replace `<triton_container_name>` with your container’s name (e.g., triton-server).

## Clean up

Detach the program by stopping the script `(Ctrl+C)`. No persistent state is written.