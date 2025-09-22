from bcc import BPF
import argparse
import os
import ctypes
from collections import defaultdict

def get_pid(container_name):
    cmd = f"docker inspect --format '{{{{.State.Pid}}}}' {container_name}"
    return int(os.popen(cmd).read().strip())

# Argument parsing
parser = argparse.ArgumentParser(description="Trace recvfrom/sendto syscalls for Triton in Docker")
parser.add_argument("-c", "--container", required=True, help="Name of the Docker container running triton")
args = parser.parse_args()

TRITON_PID = get_pid(args.container)
print(f"Tracing triton (PID {TRITON_PID}) inside container {args.container}")

# BPF Program
bpf_text = """
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>
#include <linux/uio.h>
#include <linux/socket.h>

struct data_t {
    u32 pid;
    u64 ts;
    char comm[TASK_COMM_LEN];
    int fd;
    char name[10];
};

BPF_RINGBUF_OUTPUT(events, 8);

int syscall__recvfrom(struct pt_regs *ctx, int fd, void *buf, size_t len, int flags,
                      struct sockaddr *src_addr, __u32 *addrlen) {
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    if (pid != TRITON_PID) return 0;

    struct data_t data = {};
    data.pid = pid;
    data.ts = bpf_ktime_get_ns();
    data.fd = fd;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    __builtin_memcpy(data.name, "recvfrom", 8);

    void *buf_ptr = events.ringbuf_reserve(sizeof(data));
    if (!buf_ptr) return 0;
    __builtin_memcpy(buf_ptr, &data, sizeof(data));
    events.ringbuf_submit(buf_ptr, 0);
    return 0;
}

int syscall__sendto(struct pt_regs *ctx, int fd, void *buf, size_t len, int flags,
                    const struct sockaddr *dest_addr, __u32 addrlen) {
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    if (pid != TRITON_PID) return 0;

    struct data_t data = {};
    data.pid = pid;
    data.ts = bpf_ktime_get_ns();
    data.fd = fd;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    __builtin_memcpy(data.name, "sendto", 6);

    void *buf_ptr = events.ringbuf_reserve(sizeof(data));
    if (!buf_ptr) return 0;
    __builtin_memcpy(buf_ptr, &data, sizeof(data));
    events.ringbuf_submit(buf_ptr, 0);
    return 0;
}
"""

class DataEvent(ctypes.Structure):
    _fields_ = [
        ("pid", ctypes.c_uint),
        ("ts", ctypes.c_ulonglong),
        ("comm", ctypes.c_char * 16),
        ("fd", ctypes.c_int),
        ("name", ctypes.c_char * 10),
    ]

bpf_text = bpf_text.replace("TRITON_PID", str(TRITON_PID))
b = BPF(text=bpf_text, cflags=["-w"])
b.attach_kprobe(event="__x64_sys_recvfrom", fn_name="syscall__recvfrom")
b.attach_kprobe(event="__x64_sys_sendto", fn_name="syscall__sendto")

pending_reads = defaultdict(list)

def print_event(cpu, data, size):
    event = ctypes.cast(data, ctypes.POINTER(DataEvent)).contents
    comm = bytes(event.comm).decode("utf-8", "replace").rstrip("\x00")
    name = bytes(event.name).decode("utf-8", "replace").rstrip("\x00")
    # Print a single line per event: timestamp(ns) pid comm fd syscall
    print(f"{event.ts} {event.pid} {comm} fd={event.fd} {name}")

b["events"].open_ring_buffer(print_event)
print("Printing syscalls to terminal... Press Ctrl+C to stop.")
while True:
    try:
        b.ring_buffer_poll()
    except KeyboardInterrupt:
        print("Tracing stopped.")
        break
