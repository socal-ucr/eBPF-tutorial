# Installing BCC
[BCC](https://github.com/iovisor/bcc/blob/master/INSTALL.md#ubuntu---source:~:text=%23%20For%20Noble%20Numbat%20(24.04)%0Asudo%20apt%20install%20%2Dy%20zip%20bison%20build%2Dessential%20cmake%20flex%20git%20libedit%2Ddev%20%5C%0A%20%20libllvm18%20llvm%2D18%2Ddev%20libclang%2D18%2Ddev%20python3%20zlib1g%2Ddev%20libelf%2Ddev%20libfl%2Ddev%20python3%2Dsetuptools%20%5C%0A%20%20liblzma%2Ddev%20libdebuginfod%2Ddev%20arping%20netperf%20iperf%20libpolly%2D18%2Ddev)

# Building libbpf and installing header files

- installed bpftool
- installed pkg-config 
- installed lib-elf-dev
- installed build-essential
- installed clang
- installed file

Libbpf is included as a submodule in this repo. You'll need to build and install
it for the C-based examples to build correctly. (See libbpf/README.md for more
details.)

```sh
cd libbpf/src
make install 
cd ../..
```

```sh
cd 2-HelloWorld/bpftrace
make

file hello.bpf.o
llvm-objdump-18 -S helloWorld.bpf.o

sudo bpftool prog load helloWorld.bpf.o /sys/fs/bpf/helloWorld
sudo ls /sys/fs/bpf/
sudo bpftool prog list
sudo bpftool prog show id {ID} --pretty
sudo bpftool prog dump xlated name helloWorld

sudo bpftool net list 
```

XDP is empty. Change it to syscall