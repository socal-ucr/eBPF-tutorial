from bcc import BPF
import argparse
import os

def get_pid(container_name):
    cmd = f"docker inspect --format '{{{{.State.Pid}}}}' {container_name}"
    return int(os.popen(cmd).read().strip())

# Args
parser = argparse.ArgumentParser(description="Minimal kprobe: print with bpf_printk")
parser.add_argument("-c", "--container", required=True, help="Docker container running Triton")
args = parser.parse_args()

TRITON_PID = get_pid(args.container)
print(f"Tracing Triton (PID {TRITON_PID}) inside container {args.container}")

bpf_text = r"""
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>
#include <linux/socket.h>

int syscall__recvfrom(struct pt_regs *ctx, int fd, void *buf, size_t len, int flags,
                      struct sockaddr *src_addr, __u32 *addrlen) {
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    if (pid != TRITON_PID) return 0;

    char comm[TASK_COMM_LEN];
    bpf_get_current_comm(&comm, sizeof(comm));
    bpf_trace_printk("recvfrom pid=%d fd=%d comm=%s\n", pid, fd, comm);
    return 0;
}

// TODO: Add sendto syscall tracing
int syscall__sendto(struct pt_regs *ctx, int fd, void *buf, size_t len, int flags,
                    const struct sockaddr *dest_addr, __u32 addrlen) {
    // Add your code here
    return 0;
}
""".replace("TRITON_PID", str(TRITON_PID))

# Load & attach
b = BPF(text=bpf_text, cflags=["-w"])
b.attach_kprobe(event="__x64_sys_recvfrom", fn_name="syscall__recvfrom")
# TODO: Attach kprobe to trace sendto syscall

print("Printing kprobe messages (Ctrl+C to stop)...")
# This reads from /sys/kernel/debug/tracing/trace_pipe for you
b.trace_print()

