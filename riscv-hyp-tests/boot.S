
.section .boot, "ax" 
.globl _boot
_boot:
    bnez a0, .
    csrwi    sscratch, 0xf
    /* Initialize stack pointer */
    la sp, __stack_top

    /* Clear bss */ 
    la a0, __bss_start
    la a1, __bss_end
    bgeu a0, a1, 2f
1:
    sw zero, (a0)
    addi a0, a0, 4
    bltu a0, a1, 1b
2:
    call _init
    call main
    li a0, 0
    call exit
    j .

.section ".tohost","aw",@progbits
.align 6
.globl tohost
tohost: .dword 0
.align 6
.globl fromhost
fromhost: .dword 0

.section .text

.global htif_exit
htif_exit:
    la t0, tohost
    sll a0, a0, 1
    or a0, a0, 1
1:
    sw a0, 0(t0)
    sw zero, 4(t0)
    j 1b

.global htif_putc
htif_putc:
    la t0, tohost
    sw a0, 0(t0)
    // device=1 (terminal), cmd=1 (output)
    li a0, 0x01010000
    sw a0, 4(t0)
    ret

