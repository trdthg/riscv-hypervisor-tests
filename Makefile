export PATH := $(RISCV)/bin:$(PATH)

.PHONY: riscv-hs-tests riscv-hyp-tests riscv-hext-asm-tests

build-riscv-hs-tests:
	cd riscv-hs-tests \
	&& make all
run-riscv-hs-tests:
	cd riscv-hs-tests \
	&& sail_riscv_sim --config ../rv64d_v128_e64.json ./build/riscv-hs-tests.elf --trace-all --trace-output ./log/sail_trace.log
clean-riscv-hs-tests:
	cd riscv-hs-tests \
	&& make clean

build-riscv-hyp-tests:
	cd riscv-hyp-tests \
	&& PLAT=sail LOG_LEVEL=LOG_INFO make
run-riscv-hyp-tests:
	cd riscv-hyp-tests \
	&& sail_riscv_sim --config ../rv64d_v128_e64.json ./build/sail/rvh_test.elf --trace-all --trace-output ./log/sail_trace.log
clean-riscv-hyp-tests:
	cd riscv-hyp-tests \
	&& PLAT=sail make clean

build-riscv-hext-asm-tests:
	cd riscv-hext-asm-tests \
	&& ./run_tests.py --build
run-riscv-hext-asm-tests:
	cd riscv-hext-asm-tests \
	&& ./run_tests.py --run
clean-riscv-hext-asm-tests:
	cd riscv-hext-asm-tests \
	&& ./run_tests.py --clean

build: build-riscv-hs-tests build-riscv-hyp-tests build-riscv-hext-asm-tests
run: run-riscv-hs-tests run-riscv-hyp-tests run-riscv-hext-asm-tests
clean: clean-riscv-hs-tests clean-riscv-hyp-tests clean-riscv-hext-asm-tests
