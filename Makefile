export PATH := $(RISCV)/bin:$(PATH)

.PHONY: riscv-hs-tests riscv-hyp-tests riscv-hext-asm-tests

build-riscv-hs-tests:
	cd riscv-hs-tests \
	&& make all \
	&& riscv64-unknown-elf-objdump -D ./build/riscv-hs-tests.elf  > ./log.disasm
run-riscv-hs-tests:
# 	sail_riscv_sim --config ./rv64d_v128_e64.json ./riscv-hs-tests/build/riscv-hs-tests.elf
#   qemu-system-riscv64 -M virt -kernel build/riscv-hs-tests.elf -nographic
clean-riscv-hs-tests:
	cd riscv-hs-tests \
	&& make clean

dts:
	sail_riscv_sim --print-device-tree > sail.dts
	dtc -I dts -O dtb -o sail.dtb sail.dts

build-riscv-hyp-tests:
	cd riscv-hyp-tests \
	&& PLAT=sail LOG_LEVEL=LOG_DEBUG make
run-riscv-hyp-tests:
# 	sail_riscv_sim --config ../rv64d_v128_e64.json ./build/sail/rvh_test.elf
clean-riscv-hyp-tests:
	cd riscv-hyp-tests \
	&& PLAT=sail make clean

build-riscv-hext-asm-tests:
	cd riscv-hext-asm-tests \
	&& ./run_tests.py --build
test:
	cd riscv-hext-asm-tests \
	&& ./run_tests.py -d
run-riscv-hext-asm-tests:
	cd riscv-hext-asm-tests \
	&& ./run_tests.py --run
clean-riscv-hext-asm-tests:
	cd riscv-hext-asm-tests \
	&& ./run_tests.py --clean

build: build-riscv-hs-tests build-riscv-hyp-tests build-riscv-hext-asm-tests
run: run-riscv-hs-tests run-riscv-hyp-tests run-riscv-hext-asm-tests
clean: clean-riscv-hs-tests clean-riscv-hyp-tests clean-riscv-hext-asm-tests
