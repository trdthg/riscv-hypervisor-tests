#ifndef INSTRUCTIONS_H
#define INSTRUCTIONS_H

#include <util.h>

#define INS_OPCODE  BIT_MASK(0, 7)
#define INS_RD      BIT_MASK(7, 5)
#define INS_FUNCT3  BIT_MASK(12, 3)
#define INS_RS1     BIT_MASK(15, 5)
#define INS_RS2     BIT_MASK(20, 5)
#define INS_FUNCT7  BIT_MASK(25, 7)

#define INS_C_OPCODE        BIT_MASK(0, 2)  
#define INS_C_FUNCT3_OFF    (13)
#define INS_C_FUNCT3_LEN    (3)
#define INS_C_FUNCT3_MASK   BIT_MASK(INS_C_FUNCT3_OFF, INS_C_FUNCT3_LEN)
#define INS_C_FUNCT3        INS_C_FUNCT3_MASK
#define INS_C_RS1_OFF       (7)
#define INS_C_RS1_LEN       (3)
#define INS_C_RS1_MASK      BIT_MASK(INS_C_RS1_OFF, INS_C_RS1_LEN)
#define INS_C_RDRS2_OFF     (2)
#define INS_C_RDRS2_LEN     (3)
#define INS_C_RDRS2_MASK    BIT_MASK(INS_C_RDRS2_OFF, INS_C_RDRS2_LEN)
#define INS_C_IMM0_OFF      (5)
#define INS_C_IMM0_LEN      (2)
#define INS_C_IMM0_MASK     BIT_MASK(INS_C_IMM0_OFF, INS_C_IMM0_LEN)
#define INS_C_IMM1_OFF      (10)
#define INS_C_IMM1_LEN      (3)
#define INS_C_IMM1_MASK     BIT_MASK(INS_C_IMM1_OFF, INS_C_IMM1_LEN)

#define INS_COMPRESSED(ins) (((ins) & INS_C_OPCODE) != 0b11)

#ifndef __ASSEMBLER__

#define CSR_STR(s) _CSR_STR(s)
#define _CSR_STR(s) #s

#define CSRR(csr)                                     \
    ({                                                \
        uint64_t _temp;                               \
        asm volatile("csrr  %0, " CSR_STR(csr) "\n\r" \
                     : "=r"(_temp)::"memory");        \
        _temp;                                        \
    })

#define CSRW(csr, rs) \
    asm volatile("csrw  " CSR_STR(csr) ", %0\n\r" ::"rK"(rs) : "memory")
#define CSRS(csr, rs) \
    asm volatile("csrs  " CSR_STR(csr) ", %0\n\r" ::"rK"(rs) : "memory")
#define CSRC(csr, rs) \
    asm volatile("csrc  " CSR_STR(csr) ", %0\n\r" ::"rK"(rs) : "memory")

static inline void sfence(){
    asm volatile ("sfence.vma \n\t");
}

static inline void sfence_vma(){
    
}

static inline void sfence_vmid(){
    
}

static inline void sfence_vma_vmid(){
    
}

static inline void sfence_va(){
    
}

static inline void hfence_gvma() {
    asm volatile(
        ".insn r 0x73, 0x0, 0x31, x0, x0, x0\n\t"
        ::: "memory");
}

static inline void hfence_vvma() {
    asm volatile(
        ".insn r 0x73, 0x0, 0x11, x0, x0, x0\n\t"
        ::: "memory");
}

static inline void hfence() {
    hfence_vvma();
    hfence_gvma();
}

static inline uint64_t hlvb(uintptr_t addr){
    uint64_t value;
    asm volatile(
        ".insn r 0x73, 0x4, 0x30, %0, %1, x0\n\t"
        : "=r"(value): "r"(addr) : "memory");
    return value;
}

static inline uint64_t hlvbu(uintptr_t addr){
    uint64_t value;
    asm volatile(
        ".insn r 0x73, 0x4, 0x30, %0, %1, x1\n\t"
        : "=r"(value): "r"(addr) : "memory");
    return value;
}


static inline uint64_t hlvh(uintptr_t addr){
    uint64_t value;
    asm volatile(
        ".insn r 0x73, 0x4, 0x32, %0, %1, x0\n\t"
        : "=r"(value): "r"(addr) : "memory");
    return value;
}

static inline uint64_t hlvhu(uintptr_t addr){
    uint64_t value;
    asm volatile(
        ".insn r 0x73, 0x4, 0x32, %0, %1, x1\n\t"
        : "=r"(value): "r"(addr) : "memory");
    return value;
}

static inline uint64_t hlvxhu(uintptr_t addr){
    uint64_t value;
    asm volatile(
        ".insn r 0x73, 0x4, 0x32, %0, %1, x3\n\t"
        : "=r"(value): "r"(addr) : "memory");
    return value;
}

static inline uint64_t hlvw(uintptr_t addr){
    uint64_t value;
    asm volatile(
        ".insn r 0x73, 0x4, 0x34, %0, %1, x0\n\t"
        : "=r"(value): "r"(addr) : "memory");
    return value;
}

static inline uint64_t hlvwu(uintptr_t addr){
    uint64_t value;
    asm volatile(
        ".insn r 0x73, 0x4, 0x34, %0, %1, x1\n\t"
        : "=r"(value): "r"(addr) : "memory");
    return value;
}

static inline uint64_t hlvxwu(uintptr_t addr){
    uint64_t value;
    asm volatile(
        ".insn r 0x73, 0x4, 0x34, %0, %1, x3\n\t"
        : "=r"(value): "r"(addr) : "memory");
    return value;
}

static inline uint64_t hlvd(uintptr_t addr){
    uint64_t value;
    asm volatile(
        ".insn r 0x73, 0x4, 0x36, %0, %1, x0\n\t"
        : "=r"(value): "r"(addr) : "memory");
    return value;
}

static inline uint64_t hsvb(uintptr_t addr, uint64_t value){
    asm volatile(
        ".insn r 0x73, 0x4, 0x31, x0, %1, %0\n\t"
        :: "r"(value), "r"(addr) : "memory");
    return value;
}

static inline uint64_t hsvh(uintptr_t addr, uint64_t value){
    asm volatile(
        ".insn r 0x73, 0x4, 0x33, x0, %1, %0\n\t"
        :: "r"(value), "r"(addr): "memory");
    return value;
}

static inline uint64_t hsvw(uintptr_t addr, uint64_t value){
    asm volatile(
        ".insn r 0x73, 0x4, 0x35, x0, %1, %0\n\t"
        :: "r"(value), "r"(addr): "memory");
    return value;
}

static inline uint64_t hsvd(uintptr_t addr, uint64_t value){
    asm volatile(
        ".insn r 0x73, 0x4, 0x37, x0, %1, %0\n\t"
        :: "r"(value), "r"(addr) : "memory");
    return value;
}

static inline void wfi() {
    asm ("wfi" ::: "memory");
}

#define LOAD_INSTRUCTION(name, instruction, type) \
    static inline type name(uintptr_t addr){ \
        type value; \
        asm volatile( \
            ".option push\n\t" \
            ".option norvc\n\t" \
            instruction " %0, 0(%1)\n\t" \
            ".option pop\n\t" \
            : "=r"(value) : "r"(addr) : "memory"); \
        return value; \
    }

LOAD_INSTRUCTION(lb, "lb", uint8_t);
LOAD_INSTRUCTION(lbu, "lbu", uint8_t);
LOAD_INSTRUCTION(lh, "lh", uint16_t);
LOAD_INSTRUCTION(lhu, "lhu", uint16_t); 
LOAD_INSTRUCTION(lw, "lw", uint32_t); 
LOAD_INSTRUCTION(lwu, "lwu", uint32_t);
LOAD_INSTRUCTION(ld, "ld", uint64_t);


#define STORE_INSTRUCTION(name, instruction, type) \
    static inline void name(uintptr_t addr, type value){ \
        asm volatile( \
            ".option push\n\t" \
            ".option norvc\n\t" \
            instruction " %0, 0(%1)\n\t" \
            ".option pop\n\t" \
            :: "r"(value), "r"(addr):  "memory" \
        ); \
    }

STORE_INSTRUCTION(sb, "sb", uint8_t);
STORE_INSTRUCTION(sh, "sh", uint16_t);
STORE_INSTRUCTION(sw, "sw", uint32_t);
STORE_INSTRUCTION(sd, "sd", uint64_t);

/**
 * For compressed instructions there is no constraint to guarantee
 * the asm extended chosen registers are part of the subset allowed
 * so we have to make sure.
 */

static inline uint64_t c_lw(uintptr_t addr){
    register uint64_t _addr asm("a0") = addr;
    register uint64_t value asm("a1");
    asm volatile(
        "c.lw    %0, 0(%1)\n\t"
        :"=r"(value): "r"(_addr) : "memory"
    );
    return value;
}

static inline uint64_t c_ld(uintptr_t addr){
    register uint64_t _addr asm("a0") = addr;
    register uint64_t value asm("a1");
    asm volatile(
        "c.ld    %0, 0(%1)\n\t"
        :"=r"(value): "r"(_addr) : "memory"
    );
    return value;
}

static inline void c_sw(uintptr_t addr, uint64_t value){
    register uint64_t _addr asm("a0") = addr;
    register uint64_t _value asm("a1") = value;
    asm volatile(
        "c.sw    %0, 0(%1)\n\t"
        :: "r"(_value), "r"(_addr): "memory"
    );
}

static inline void c_sd(uintptr_t addr, uint64_t value){
    register uint64_t _addr asm("a0") = addr;
    register uint64_t _value asm("a1") = value;
    asm volatile(
        "c.sd    %0, 0(%1)\n\t"
        :: "r"(_value), "r"(_addr): "memory"
    );
}

static inline uint32_t lr_w(uintptr_t addr){
    uint32_t value;
    asm volatile(
        "lr.w %0, 0(%1)\n\t"
        : "=r"(value) : "r"(addr): "memory"
    );
    return value;
}

static inline uint32_t sc_w(uintptr_t addr, uint64_t value){
    asm volatile(
        "sc.w    %0, %0, 0(%1)\n\t"
        : "+r"(value) : "r"(addr): "memory"
    );
    return value;
}

#define AMO_INSTRUCTION(name, instruction, type) \
    static inline type name(uintptr_t addr, type value){ \
        asm volatile( \
            instruction " %0, %0, 0(%1)\n\t" \
            : "+r"(value) : "r"(addr): "memory" \
        ); \
        return value; \
    }

AMO_INSTRUCTION(amoswap_w, "amoswap.w", uint32_t);
AMO_INSTRUCTION(amoadd_w, "amoadd.w", uint32_t);
AMO_INSTRUCTION(amoxor_w, "amoxor.w", uint32_t);
AMO_INSTRUCTION(amoand_w, "amoand.w", uint32_t);
AMO_INSTRUCTION(amoor_w, "amoor.w", uint32_t);
AMO_INSTRUCTION(amomin_w, "amomin.w", uint32_t);
AMO_INSTRUCTION(amomax_w, "amomax.w", uint32_t);
AMO_INSTRUCTION(amominu_w, "amominu.w", uint32_t);
AMO_INSTRUCTION(amomaxu_w, "amomaxu.w", uint32_t);
AMO_INSTRUCTION(amoswap_d, "amoswap.d", uint64_t);
AMO_INSTRUCTION(amoadd_d, "amoadd.d", uint64_t);
AMO_INSTRUCTION(amoxor_d, "amoxor.d", uint64_t);
AMO_INSTRUCTION(amoand_d, "amoand.d", uint64_t);
AMO_INSTRUCTION(amoor_d, "amoor.d", uint64_t);
AMO_INSTRUCTION(amomin_d, "amomin.d", uint64_t);
AMO_INSTRUCTION(amomax_d, "amomax.d", uint64_t);
AMO_INSTRUCTION(amominu_d, "amominu.d", uint64_t);
AMO_INSTRUCTION(amomaxu_d, "amomaxu.d", uint64_t);

#endif /* __ASSEMBLER__ */

#endif /* INSTRUCTIONS_H */
