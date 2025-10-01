# Installing BCC

# Building libbpf and installing header files

Libbpf is included as a submodule in this repo. You'll need to build and install
it for the C-based examples to build correctly. (See libbpf/README.md for more
details.)

```sh
cd libbpf/src
make install 
cd ../..
```