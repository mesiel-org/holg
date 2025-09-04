#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

# Paths
holg_bin = Path(__file__).parent.parent / "target/release/holg"
input_dirs = [Path("./tests/arena/"), Path("./tests/malloc/")]
output_file = Path("./tests/output.h")
main_c = Path("./tests/main.c")
exe_file = Path("./tests/test_exe")

def run_holg():
    """If HOLG is not found, build it"""
    if not holg_bin.exists():
        print("Error: HOLG binary not found")
        print("Building HOLG...")
        subprocess.run(["python3", "ci/build.py", "--host-only"], check=True)
    print("HOLG binary found:", holg_bin)
    """Run HOLG to generate the header"""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    cmd = [str(holg_bin)]
    cmd.extend([str(d) for d in input_dirs])
    cmd.extend(["-o", str(output_file)])
    print("Running HOLG:", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("HOLG failed:\n", result.stderr)
        sys.exit(1)
    print("HOLG generated header successfully.")

def compile_c():
    """Compile main.c with Clang including the generated header"""
    if not output_file.exists():
        print("Error: output.h not found")
        sys.exit(1)
    cmd = ["clang", "-I", str(output_file.parent), "-o", str(exe_file), str(main_c)]
    print("Compiling C code:", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Compilation failed:\n", result.stdout, result.stderr)
        sys.exit(1)
    print("Compilation successful.")

def run_executable():
    """Run the compiled executable"""
    print("Running executable:", exe_file)
    result = subprocess.run([str(exe_file)], capture_output=True, text=True)
    if result.returncode != 0:
        print("Execution failed:\n", result.stdout, result.stderr)
        sys.exit(1)
    print("Execution output:\n", result.stdout)

if __name__ == "__main__":
    run_holg()
    compile_c()
    run_executable()
    print("HOLG test passed successfully!")
