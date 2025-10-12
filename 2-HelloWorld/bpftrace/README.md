# Creating the eBPF byte code and loding the program using bpftrace

In this section, you’ll learn how to write, compile, and load a simple eBPF program into the Linux kernel.

[bpftrace](https://github.com/bpftrace/bpftrace) is already installed in the servers given to you.
Please visit [bpftrace](https://github.com/bpftrace/bpftrace) github for more information.

If you’d like to learn more about the tools, refer to the [bpftrace GitHub page](https://github.com/bpftrace/bpftrace) and the [bpftool documentation](https://bpftool.dev/).

## Starting with bpftrace

You can check that `bpftrace` is installed and working properly by running:
```sh
bpftrace --version
```
This should print the installed version number.

## Writing a Simple eBPF Program
Let’s start with `helloWorld.bpf.c` a minimal program that prints `"Hello World"` every time a packet passes through the interface. 
```C
#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>

int counter = 0;

SEC("xdp")
int helloWorld(struct xdp_md *ctx) {
    bpf_printk("Hello World %d", counter);
    counter++;
    return XDP_PASS;
}

char LICENSE[] SEC("license") = "Dual BSD/GPL";
```

### Breakdown of the Code

- `SEC("xdp")`: Places the program in the XDP section, so it can be attached to a network interface.

- `bpf_printk()`: Prints messages to the kernel trace buffer (/sys/kernel/debug/tracing/trace_pipe).

- `XDP_PASS`: Allows packets to continue through the normal network stack.

- `counter`: A simple global integer incremented on each packet to demonstrate persistence.

- `char LICENSE[]`: Specifies the license required for kernel compatibility.

## Compiling the eBPF Program

eBPF programs must be compiled into **bytecode** that the eBPF virtual machine can understand.
We use **Clang** (from LLVM) to compile the program to a `.o` object file.
Using the `Makefile` provided in this directory, just run:
```sh
make
```

## Inspecting the Compiled eBPF Object File

Check that your compiled file is indeed an eBPF object:
```sh
file helloWorld.bpf.o
```

You can disassemble it to view the actual eBPF bytecode using `llvm-objdump`:
```sh
llvm-objdump-18 -S helloWorld.bpf.o
```
This will show the assembly instructions that will run inside the eBPF virtual machine.

## Loading the Program into the Kernel

Now, let’s load the program into the kernel before attaching it to a network interface.
```sh
sudo bpftool prog load helloWorld.bpf.o /sys/fs/bpf/helloWorld
```

Check that it was successfully loaded:

```sh
sudo ls /sys/fs/bpf/
```

The bpftool utility can list all the programs that are loaded into the kernel. If you try this yourself you’ll probably see several preexisting eBPF programs in this output:
```sh
sudo bpftool prog list
```

You can also filter these programs by name to only list our helloWorld program:
```sh
sudo bpftool prog list name helloWorld
```

Our helloWorld program will be assigned a unique **$ID$**. Extract this **$ID$** from the output of `sudo bpftool prog list name helloWorld` to use for the rest of the experiment. 

This identity is a number assigned to each program as it’s loaded. Knowing the ID, you can ask bpftool to show more information about this program. This time, let’s get the output in prettified JSON format so that the field names are visible, as well as the values:
```sh
sudo bpftool prog show id $ID$ --pretty
```

You can also see the translated instructions:
```sh
sudo bpftool prog dump xlated name helloWorld
```

## Attaching the Program
We first need to find a network interface to attach our XDP program too. To find your network interfaces:
```sh
ip link
```

Then attach your eBPF program to the loopback interface:
```sh
sudo bpftool net attach xdp id {ID} dev lo
```

Confirm it’s attached:
```sh
sudo bpftool net list 
```

## Output
The bpf_printk output is written to the kernel tracing buffer. You can view it in real time:
```sh
sudo cat /sys/kernel/debug/tracing/trace_pipe
```

## Inspecting Maps
You can list eBPF maps, in our case the global variable `counter`, currently loaded in the kernel:
```sh
sudo bpftool map list
```

## Detaching and Cleaning Up
When done, detach the program and clean up the pinned object:
```sh
sudo bpftool net detach xdp dev lo
sudo rm /sys/fs/bpf/helloWorld
```
This ensures your kernel and BPF filesystem stay clean.
