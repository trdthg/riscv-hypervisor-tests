# Run tests on spike emulator
# 
# Assumes sail_riscv_sim is in PATH

# Build tests
make clean
export PLAT=sail LOG_LEVEL=LOG_WARNING
make

# Run tests
# spike -l --log-commits --log=log/spike_trace.log --isa=RV64gch build/spike/rvh_test.elf &> log/spike_term.log
sail_riscv_sim --config ../rv64d_v128_e64.json ./build/sail/rvh_test.elf &> log/sail_term.log