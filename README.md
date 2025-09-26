# RISC-V Hypervisor Tests

## About

This repository contains a collection of tests for the RISC-V Hypervisor Extension. Currently, the following repositories are included:

- [riscv-hyp-tests](https://github.com/defermelowie/riscv-hyp-tests)
    - add script/run_on_sail.sh
- [riscv-hs-tests](https://github.com/dramforever/riscv-hs-tests)
    - fix function args
- [riscv-hext-asm-tests](https://github.com/defermelowie/riscv-hext-asm-tests)
    - inline submodule asm-tests

Note: these repo are not included as submodule but copied for convenience

## Build

1. prepare riscv-gnu-toolchain, and `RISCV` environment variable

    Note: riscv-gcc from ubuntu apt 

2. run `make build-all`

## Run

- [riscv-hyp-tests](https://github.com/defermelowie/riscv-hyp-tests)
    - `make run-riscv-hyp-tests`
- [riscv-hs-tests](https://github.com/dramforever/riscv-hs-tests)
    - `make run-riscv-hs-tests`
- [riscv-hext-asm-tests](https://github.com/defermelowie/riscv-hext-asm-tests)
    - `make run-riscv-hext-asm-tests`

Run all: `make run-all`
