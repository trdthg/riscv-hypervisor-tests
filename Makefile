export PATH := $(RISCV)/bin:$(PATH)

.PHONY: riscv-hs-tests riscv-hyp-tests riscv-hext-asm-tests

build-riscv-hs-tests:
	cd riscv-hs-tests \
	&& make all
run-riscv-hs-tests:
	riscv-hs-tests/build/riscv-hs-tests.elf
clean-riscv-hs-tests:
	cd riscv-hs-tests \
	&& make clean

build-riscv-hyp-tests:
	cd riscv-hyp-tests \
	&& PLAT=spike make
run-riscv-hyp-tests:
	cd riscv-hyp-tests \
	&& ./scripts/run_on_sail.sh
clean-riscv-hyp-tests:
	cd riscv-hyp-tests \
	&& PLAT=spike make clean

build-riscv-hext-asm-tests:
	cd riscv-hext-asm-tests \
	&& ./run_tests.py --build
run-riscv-hext-asm-tests:
	cd riscv-hext-asm-tests \
	&& ./run_tests.py
clean-riscv-hext-asm-tests:
	cd riscv-hext-asm-tests \
	&& ./run_tests.py --clean

build: build-riscv-hs-tests build-riscv-hyp-tests build-riscv-hext-asm-tests
run: run-riscv-hs-tests run-riscv-hyp-tests run-riscv-hext-asm-tests
clean: clean-riscv-hs-tests clean-riscv-hyp-tests clean-riscv-hext-asm-tests
