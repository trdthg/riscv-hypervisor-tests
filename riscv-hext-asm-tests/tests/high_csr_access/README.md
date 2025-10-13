Specifically, a virtual-instruction exception is raised for the following cases:

## VS/VU Counter CSR

- in VS-mode, attempts to access a non-high-half counter CSR when the corresponding bit in hcounteren is 0 and the same bit in mcounteren is 1;
- in VS-mode, if XLEN=32, attempts to access a high-half counter CSR when the corresponding bit in hcounteren is 0 and the same bit in mcounteren is 1;
- in VU-mode, attempts to access a non-high-half counter CSR when the corresponding bit in either hcounteren or scounteren is 0 and the same bit in mcounteren is 1;
- in VU-mode, if XLEN=32, attempts to access a high-half counter CSR when the corresponding bit in either hcounteren or scounteren is 0 and the same bit in mcounteren is 1;

## VS/VU half, TVM
- in VS-mode or VU-mode, attempts to access an implemented non-high-half hypervisor CSR or VS CSR when the same access (read/write) would be allowed in HS-mode, assuming mstatus.TVM=0;
- in VS-mode or VU-mode, if XLEN=32, attempts to access an implemented high-half hypervisor CSR or high-half VS CSR when the same access (read/write) to the CSR"s low-half partner would be allowed in HS-mode, assuming mstatus.TVM=0;
- in VU-mode, attempts to access an implemented non-high-half supervisor CSR when the same access (read/write) would be allowed in HS-mode, assuming mstatus.TVM=0;
- in VU-mode, if XLEN=32, attempts to access an implemented high-half supervisor CSR when the same access to the CSR’s low-half partner would be allowed in HS-mode, assuming mstatus.TVM=0;

## execute

### H_insts
- in VS-mode or VU-mode, attempts to execute a hypervisor instruction (HLV, HLVX, HSV, or HFENCE);

### WFI, TW
- in VU-mode, attempts to execute WFI when mstatus.TW=0, or to execute a supervisor instruction (SRET or SFENCE);
in VS-mode, attempts to execute WFI when hstatus.VTW=1 and mstatus.TW=0, unless the instruction completes within an implementation-specific, bounded time;

### SRET, VSTR
in VS-mode, attempts to execute SRET when hstatus.VTSR=1; and

### SFENCE/SINVAL, VMA
in VS-mode, attempts to execute an SFENCE.VMA or SINVAL.VMA instruction or to access satp, when hstatus.VTVM=1.

### Privilege
- Other extensions to the RISC-V Privileged Architecture may add to the set of circumstances that cause a virtual-instruction exception when V=1.
- On a virtual-instruction trap, mtval or stval is written the same as for an illegal-instruction trap.
