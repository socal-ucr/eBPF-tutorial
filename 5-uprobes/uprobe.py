from bcc import BPF
import argparse
import os

def get_pid(container_name):
    cmd = f"docker inspect --format '{{{{.State.Pid}}}}' {container_name}"
    return int(os.popen(cmd).read().strip())

def attach_uprobe_grpc_core(bpf, pid):
    triton_binary = "/var/lib/docker/overlay2/b49f62eb49d20d5cd2c849cd4b81e4777bb042a4924376786e74cc113f8b210f/diff/opt/tritonserver/bin/tritonserver"   
    metadata_symbol = "_Z49grpc_chttp2_maybe_complete_recv_trailing_metadataP21grpc_chttp2_transportP18grpc_chttp2_stream"
    bpf.attach_uprobe(name=triton_binary, sym=metadata_symbol, fn_name="trace_metadata_func")

# Define the BPF program
bpf_text = """
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

// Uprobe: grpc_chttp2_maybe_complete_recv_trailing_metadata
int trace_metadata_func(struct pt_regs *ctx) {
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    if (pid != PID) return 0;

    bpf_trace_printk("gRPC Metadata Function Called - PID: %d\\n", pid);
    return 0;
}
"""

def init_benchmark(container_name):
    pid = get_pid(container_name)
    print(f"Initializing tracing for container '{container_name}' (PID {pid})")
    bpf = BPF(text=bpf_text.replace("PID", str(pid)), cflags=["-w"])
    attach_uprobe_grpc_core(bpf, pid)
    return bpf

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trace gRPC function calls")
    parser.add_argument("-c", "--container", required=True, help="Container name")
    args = parser.parse_args()

    try:
        bpf = init_benchmark(args.container)
        print("Tracing gRPC function calls... Press Ctrl+C to stop.")
        
        # Start the BPF program and print events to the terminal
        bpf.trace_print()
    except Exception as e:
        print(f"[ERROR] Error while tracing: {e}")
