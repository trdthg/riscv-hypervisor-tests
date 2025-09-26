#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Dict, List
from pathlib import Path
import logging as log
import yaml
import argparse
import subprocess

# ------------------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------------------

ALL_TESTS = [
    # "ci_direct_fail",   # For CI debug only
    # "ci_infinite_loop", # For CI debug only
    "h_ext_enabled",
    "h_ext_csr_defined",
    # "htif_fromhost",     # Manual inspection only
    # "htif_getc",         # Manual inspection only
    "mret_M_to_HS",
    "mret_M_to_U",
    "mret_M_to_VS",
    "mret_M_to_VU",
    "sret_HS_to_U",
    "sret_HS_to_VS",
    "sret_HS_to_VU",
    "sret_VS_to_VU",
    "ecall_HS_to_M",
    "ecall_U_to_HS",
    "ecall_U_to_M",
    "ecall_VS_to_HS",
    "ecall_VS_to_M",
    "ecall_VU_to_HS",
    "ecall_VU_to_M",
    "ecall_VU_to_VS",
    "read_h_csr_from_U",
    "read_h_csr_from_VS",
    "read_h_csr_from_VU",
    "read_s_csr_from_U",
    "read_s_csr_from_VS",
    "read_s_csr_from_VU",
    "read_vs_csr_from_U",
    "read_vs_csr_from_VS",
    "read_vs_csr_from_VU",
    "vs_csr_substitute_s_csr",
    "vmem_S_at_independent_from_vsatp",
    "vmem_U_at_independent_from_vsatp",
    "vmem_VS_at_independent_from_satp",
    "vmem_VU_at_independent_from_satp",
    "at_S_U_39",
    "at_S_39_update_pte_A",
    "at_S_39_update_pte_D",
    "at_S_U_48",
    # "at_S_U_57", # Unsupported by Sail
    "slat_HS_39_VS_VU_39",
    "slat_VS_39_update_pte_A",
    "slat_VS_39_update_pte_D",
    "slat_HS_39_VS_39_gpage_fault",
    "slat_VS_39_pseudoinst",
    "slat_HS_39_VS_VU_48",
    # "slat_HS_39_VS_VU_57", # Unsupported by Sail
    "slat_HS_48_VS_VU_39",
    "slat_HS_48_VS_VU_48",
    "hlv_M",
    "hlv_HS_spvp_0",
    "hlv_HS_spvp_1",
    "hlv_U_spvp_0",
    "hlv_U_spvp_1",
    "hlvx_M",
    "tinst_amo",
    "tinst_load",
    "tinst_store",
    "tinst_vm_load_store",
    "high_half_CRS_ill_instr",
    "hfence_vvma_ill_inst",
    "hfence_gvma_ill_inst",
    "hsv_ill_inst",
    "hlv_ill_inst",
    "hfence_vvma_virt_inst",
    "hfence_gvma_virt_inst",
    "hsv_virt_inst",
    "hlv_virt_inst",
    "htime_delta",
    "MTI_VU_to_M",
    "MSI_VU_to_M",
    "STI_VU_to_HS",
    "SSI_VU_to_HS",
    "SEI_VU_to_HS",
    "VSSI_VU_to_HS",
    "VSTI_VU_to_VS",
    "VSSI_VU_to_VS",
    "VSEI_VU_to_VS",
    "wfi_M",
    "wfi_HS",
    "wfi_VS",
    "xip_writable_bits",
    "xie_writable_bits",
    "hgeie_writable_bits",
]

TESTDIR = Path("tests")

SAILCOV_SOURCES = list(Path("../sail-riscv/model/").glob("*.sail"))
SAILCOV_BANCHES = Path("../sail-riscv/generated_definitions/c/all_branches")

# ------------------------------------------------------------------------------
# Emulators
# ------------------------------------------------------------------------------


class Emulator(ABC):
    @abstractmethod
    def run(self, executable: Path, outdir: Path) -> bool:
        """Run test `executable`, log to `outdir/trace.log` and return success/failure"""
        pass

    @abstractmethod
    def build_vars(self) -> Dict[str, str]:
        """Return environment variables that should be used when building for this emulator"""


class SailCSim(Emulator):
    sim = Path("../sail-riscv/c_emulator/riscv_sim_RV64")
    simflags = [
        "--enable-pmp",
        "--enable-dirty-update",
        "--mtval-has-illegal-inst-bits",
        "--xtinst-has-transformed-inst",
    ]
    timeout = 5

    def __init__(self, cov: bool) -> None:
        self.cov = cov
        super().__init__()

    def run(self, executable: Path, outdir: Path) -> bool:
        covflag = f"-c {outdir.joinpath('sail_model.cov')}" if self.cov else ""
        cmd = f"{self.sim} {' '.join(self.simflags)} {covflag} {executable}"
        logfile = outdir.joinpath("trace.log")
        log.debug(f"Emulator cmd: \"{cmd}\"")
        try:
            with open(logfile, "wb") as logf:
                subprocess.run(cmd, shell=True, stderr=logf,
                               stdout=logf, timeout=self.timeout, input=b"hello\n")
            with open(logfile, "r") as logf:
                return ("SUCCESS" in logf.read())
        except subprocess.TimeoutExpired:
            log.debug(f"{cmd} timed out")
            with open(logfile, "a") as logf:
                logf.write(f"TIMEOUT: {self.timeout}")
            return False

    def build_vars(self):
        # No special environment variables required for sail
        return {}


class SailOSim(Emulator):
    sim = Path("../sail-riscv/ocaml_emulator/riscv_ocaml_sim_RV64")
    simflags = [
        "-enable-hext",
        "-enable-pmp",
        "-enable-dirty-update",
        "-mtval-has-illegal-inst-bits",
        "-xtinst-has-transformed-inst",
    ]
    timeout = 5

    def run(self, executable: Path, outdir: Path) -> bool:
        cmd = f"{self.sim} {' '.join(self.simflags)} {executable}"
        logfile = outdir.joinpath("trace.log")
        log.debug(f"Emulator cmd: \"{cmd}\"")
        try:
            with open(logfile, "wb") as logf:
                subprocess.run(cmd, shell=True, stderr=logf,
                               stdout=logf, timeout=self.timeout, input=b"hello\n")
            with open(logfile, "r") as logf:
                return ("SUCCESS" in logf.read())
        except subprocess.TimeoutExpired:
            log.debug(f"{cmd} timed out")
            with open(logfile, "a") as logf:
                logf.write(f"TIMEOUT: {self.timeout}")
            return False

    def build_vars(self):
        # No special environment variables required for sail
        return {}


class Spike(Emulator):
    sim = Path("spike")
    simflags = [
        "-l", "--log-commits",
        "--isa=RV64gch_Svadu_Zicntr",
    ]
    env = {
        "RISCV_SVADU": "true"
    }
    timeout = 5

    def run(self, executable: Path, outdir: Path) -> bool:
        cmd = f"{self.sim} {' '.join(self.simflags)} {executable}"
        logfile = outdir.joinpath("trace.log")
        log.debug(f"Emulator cmd: \"{cmd}\"")
        try:
            with open(logfile, "wb") as logf:
                res = subprocess.run(
                    cmd, shell=True, stderr=logf, stdout=logf, timeout=self.timeout, input=b"hello\n")
            return res.returncode == 0
        except subprocess.TimeoutExpired:
            log.debug(f"{cmd} timed out")
            with open(logfile, "a") as logf:
                logf.write(f"TIMEOUT: {self.timeout}")
            return False

    def build_vars(self):
        return self.env


class Qemu(Emulator):
    sim = Path("qemu-system-riscv64")
    simflags = [
        "--machine", "spike",
        "-cpu", "rv64,h=true",
        "-d", "in_asm,int,cpu",
        "-nographic",
    ]
    timeout = 5

    def run(self, executable: Path, outdir: Path) -> bool:
        cmd = f"{self.sim} {' '.join(self.simflags)} -bios {executable}"
        logfile = outdir.joinpath("trace.log")
        log.debug(f"Emulator cmd: \"{cmd}\"")
        try:
            with open(logfile, "wb") as logf:
                res = subprocess.run(
                    cmd, shell=True, stderr=logf, stdout=logf, timeout=self.timeout, input=b"hello\n")
            return res.returncode == 0
        except subprocess.TimeoutExpired:
            log.debug(f"{cmd} timed out")
            with open(logfile, "a") as logf:
                logf.write(f"TIMEOUT: {self.timeout}")
            return False

    def build_vars(self):
        return {}

# ------------------------------------------------------------------------------
# Build & run script
# ------------------------------------------------------------------------------


def main(tests: List[str], c: bool, b: bool, d: bool, r: bool, e: Emulator, cov: bool):
    success = True
    print(f"---------------------")
    # Clean tests
    if c:
        success &= clean()
    # Build tests
    if b:
        for test in tests:
            success &= build(test, e.build_vars())
        print(f"---------------------")
    # Objdump tests
    if d:
        for test in tests:
            success &= dump(test)
    # Run tests on emulator
    if r:
        passed = 0
        failed = 0
        for test in tests:
            if run(test, e):
                passed += 1
            else:
                failed += 1
        print(f"---------------------")
        print(f"[TEST RESULTS]")
        print(f"  Passed: {passed}")
        print(f"  Failed: {failed}")
        print(f"  Total:  {len(tests)}")
        print(f"---------------------")
        success &= (len(tests) == passed)
    # Create coverage report
    if cov:
        success &= coverage(tests, SAILCOV_SOURCES, SAILCOV_BANCHES)
    # Exit this script
    if success:
        exit(0)
    else:
        exit(-1)


def build(test: str, env: Dict[str, str]) -> bool:
    """Build a test"""
    test_dir = TESTDIR.joinpath(test)
    # Load build.json from test dir
    with open(test_dir.joinpath("build.yaml"), "r") as buildfile:
        MkBuilder = MakefileBuilder(yaml.safe_load(buildfile)['makefile'])
        # Build test executable
        if MkBuilder.make(test, env, test_dir.joinpath("build.log")):
            print(f"[BUILD] {test} - \x1b[32mDone\x1b[0m")
            return True
        else:
            print(f"[BUILD] {test} - \x1b[31mError\x1b[0m")
            return False


def dump(test: str) -> bool:
    """Create object dump of test"""
    elf = TESTDIR.joinpath(test, f"{test}.elf")
    dmp = TESTDIR.joinpath(test, f"{test}.dump")
    if not elf.exists():
        log.error(f"Could not find {elf}")
        return False
    else:
        subprocess.run(
            f"riscv64-unknown-elf-objdump -D {elf} > {dmp}", shell=True)
        return dmp.exists()


def clean() -> bool:
    # TODO: This can probably be more elegant using os library
    # Delete objects
    log.info("Removing all objects")
    subprocess.run("find . -name '*.o' -type f -delete",
                   shell=True)
    # Delete executables
    log.info("Removing all executables")
    subprocess.run("find . -name '*.elf' -type f -delete",
                   shell=True)
    # Delete logs
    log.info("Removing all logs")
    subprocess.run("find . -name '*.log' -type f -delete",
                   shell=True)
    # Delete coverage info
    log.info("Removing coverage info")
    subprocess.run("find . -name '*.cov' -type f -delete",
                   shell=True)
    subprocess.run("find . -name '*.html' -type f -delete",
                   shell=True)
    # Always return success
    return True


def coverage(tests: List[str], model_src: List[Path], branch_all: Path) -> bool:
    """Build coverage raport for test"""
    branches_taken = [TESTDIR.joinpath(
        test, 'sail_model.cov').absolute() for test in tests]
    branches_all = branch_all.absolute()

    cmd = f"mkdir -p coverage"
    cmd += f" && cd coverage"
    cmd += f" && sailcov -a {branches_all} {' '.join([f'-t {t}' for t in branches_taken])}"
    cmd += f" --nesting-darkness 1 --index index --histogram"
    cmd += f" {' '.join([ str(src.absolute()) for src in model_src])}"
    res = subprocess.run(cmd, shell=True, capture_output=True)
    log.debug(cmd)
    if res.returncode != 0:
        log.error(f"Sailcov error during \"{cmd}\"\n\n{res.stderr.decode('utf-8')}")
    return True


def run(test: str, emul: Emulator) -> bool:
    """Run test on specified emulator, return True on success"""
    elf = TESTDIR.joinpath(test, f"{test}.elf")
    outdir = TESTDIR.joinpath(test)
    if not elf.exists():
        log.error(f"Could not find {elf}")
        pass
    res = emul.run(elf, outdir)

    if res:
        print(f"[TEST] {test} - \x1b[32mPassed\x1b[0m")
        return True
    else:
        print(f"[TEST] {test} - \x1b[31mFailed\x1b[0m")
        return False


class MakefileBuilder():
    """Build Makefile targets using GNU make"""
    _path: Path
    _target: str
    _variables: Dict[str, str]

    def __init__(self, obj: dict):
        """Create instance from dictionary"""
        if not isinstance(obj, dict):
            raise Exception(
                "Could not create MakefileBuilder from non-dict object")

        self._path = Path(obj['path'])
        self._target = obj['target']

        self._variables = {}
        if 'variables' in obj:
            for var in obj['variables']:
                self._variables.update(var.items())

    def _vars(self, var_dict):
        if len(var_dict) == 0:
            return ''
        else:
            vars = [f"{key}={val}" for (key, val) in var_dict.items()]
            return ' '.join(vars)

    def make(self, test: str, env_vars: Dict[str, str], logpath: Path):
        with open(logpath, "wb") as logfile:
            try:
                cmd = f"make -f {self._path} {self._target} {self._vars(self._variables)} {self._vars(env_vars)}"
                log.debug(f"Build cmd: {cmd}")
                subprocess.run(cmd, shell=True, stdout=logfile,
                               stderr=logfile, check=True)
                return True
            except subprocess.CalledProcessError:
                log.error(
                    f"Build failed for {test}, check {logfile.name} for more details")
                return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Build & run test binaries')
    parser.add_argument("-c", "--clean", action='store_true',
                        help="Clean before build")
    parser.add_argument("-b", "--build", action='store_true',
                        help="Build test executables")
    parser.add_argument("-d", "--dump", action='store_true',
                        help="Create objdump of test executables")
    parser.add_argument("-r", "--run", action='store_true',
                        help="Run test executables")
    parser.add_argument("-e", "--emulator", type=str,
                        help="Run with specific emulator (default: %(default)s)", default="sail-csim")
    parser.add_argument("--cov", action='store_true',
                        help="Collect coverage info (sail-csim only)")
    parser.add_argument('-t', '--tests', nargs='+',
                        help="Run specific tests", default=ALL_TESTS)
    parser.add_argument("-v", action="count", default=0,
                        help="Enable verbose output")
    args = parser.parse_args()

    # Set log level
    verbosity = log.ERROR - (args.v * 10)
    log.basicConfig(format="[%(levelname)s] %(message)s", level=verbosity)

    # Get emulator
    emul: Emulator
    match args.emulator:
        case "sail-csim":
            log.info("Using sail C emulator")
            emul = SailCSim(args.cov)
        case "sail-osim":
            log.info("Using sail OCaml emulator")
            emul = SailOSim()
        case "spike":
            log.info("Using spike emulator")
            emul = Spike()
        case "qemu":
            log.info("Using QEMU")
            emul = Qemu()
        case other:
            log.error(f"Unknown emulator with name \"{other}\"")
            exit(-1)

    # Run main function (after argument parsing is complete)
    main(args.tests, args.clean, args.build,
         args.dump, args.run, e=emul, cov=args.cov)
