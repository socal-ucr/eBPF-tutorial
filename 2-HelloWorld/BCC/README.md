# Writing and Running Your First eBPF Program with BCC (BPF Compiler Collection)

In this section, we’ll use [**BCC (BPF Compiler Collection)**](https://github.com/iovisor/bcc/tree/v0.35.0) to load and run a simple eBPF program from user space.

BCC provides convenient Python and C++ APIs to write, compile, and attach eBPF programs dynamically, making it easier to prototype and explore kernel events.

## Verifying Installation

BCC is already installed on the provided server.
To confirm simply run,
```sh
sudo python3
```

and then import bcc by typing,
```python
from bcc import BPF
```
If it imports without errors, BCC is ready to use.

Or you can refer the `helloWorld.py` file.

## Understanding the Code

The file **`helloWorld.py`** contains a simple program that prints `"Hello World!"` from the eBPF space.
```python
#!/usr/bin/python3  
from bcc import BPF
import sys

program = r"""
int hello(void *ctx) {
    bpf_trace_printk("Hello World!");
    return 0;
}
"""

b = BPF(text=program)
syscall = b.get_syscall_fnname("execve")
b.attach_kprobe(event=syscall, fn_name="hello")

try:
    b.trace_print()
except KeyboardInterrupt:
    sys.exit(0)
```

Let’s break it down step by step:

### 1. Importing BCC

```python
from bcc import BPF
```
Imports the **BPF** class, the main interface for defining and loading eBPF programs.

### 2. Writing the eBPF Program

```c
int hello(void *ctx) {
    bpf_trace_printk("Hello World!");
    return 0;
}
```
This small C function is our eBPF program.
It runs inside the kernel and prints `"Hello World!"` whenever triggered.

### 3. Loading and Attaching the Program

```python
b = BPF(text=program)
syscall = b.get_syscall_fnname("execve")
b.attach_kprobe(event=syscall, fn_name="hello")
```

* `BPF(text=program)` compiles the C code into eBPF bytecode and loads it into the kernel.
* `get_syscall_fnname("execve")` resolves the name of the `execve` system call for the current kernel (since syscall names differ across architectures).
* `attach_kprobe()` attaches our eBPF program to that syscall.
  → The function will run every time a process executes a new command (`execve`).

### 4. Printing Kernel Messages

```python
b.trace_print()
```

This continuously reads from `/sys/kernel/debug/tracing/trace_pipe` and prints any `bpf_trace_printk()` output to your terminal.

### 5. Stopping the Program

Press **`Ctrl + C`** to stop it safely:

```python
except KeyboardInterrupt:
    sys.exit(0)
```

## Running the Program

Run your Python script with root privileges:

```bash
sudo python3 hello_bcc.py
```

Then, in a separate terminal, try running a few commands like:

```bash
ls
echo test
```

Each time a command executes, your eBPF program will trigger.


## How It Works

1. The **BCC library** compiles your C code into eBPF bytecode at runtime using LLVM.
2. The bytecode is then **loaded into the kernel** via the eBPF subsystem.
3. When the **`execve` syscall** runs, the attached probe executes your function.
4. The message from `bpf_trace_printk()` is written to the kernel trace buffer and read back by `b.trace_print()`.

## Cleaning Up

When you press `Ctrl + C`, the program automatically detaches the probe and exits cleanly.

