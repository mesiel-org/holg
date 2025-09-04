#!/usr/bin/env python3
import subprocess, sys, os, platform, shutil, tarfile, zipfile

host_only = "--host-only" in sys.argv
system = platform.system().lower()
version = os.getenv("GITHUB_REF_NAME", "dev")

targets = {
    "linux": [
        "x86_64-unknown-linux-gnu",
        "x86_64-unknown-linux-musl",
        "aarch64-unknown-linux-gnu",
        "aarch64-unknown-linux-musl",
    ],
    "darwin": [
        "x86_64-apple-darwin",
        "aarch64-apple-darwin",
    ],
    "windows": [
        "x86_64-pc-windows-msvc",
        "aarch64-pc-windows-msvc",
    ],
}

def run(cmd, env=None):
    print("Running:", " ".join(cmd))
    r = subprocess.run(cmd, env=env)
    if r.returncode != 0:
        sys.exit(f"Command failed: {' '.join(cmd)}")

def install_targets(tlist):
    for t in tlist:
        run(["rustup", "target", "add", t])

def zig_available():
    return shutil.which("zig") is not None and shutil.which("cargo-zigbuild") is not None


def build_target(target=None, use_zig=False):
    env = os.environ.copy()
    # env["RUSTFLAGS"] = "-C strip=symbols"

    if target is None:
        run(["cargo", "build", "--release"], env)
        return

    if use_zig:
        run(["cargo", "zigbuild", "--release", "--target", target], env)
    else:
        run(["cargo", "build", "--release", "--target", target], env)

def package_binary(version, target):
    outdir = os.path.join("target", target, "release")
    bin_name = "holg.exe" if target.endswith("windows-msvc") else "holg"
    bin_path = os.path.join(outdir, bin_name)

    if not os.path.exists(bin_path):
        print(f"[!] Binary not found for {target}, skipping package.")
        return

    os.makedirs("build", exist_ok=True)
    archive_name = f"holg-{version}-{target}"

    extra_files = []
    for fname in ["README.md", "LICENSE"]:
        if os.path.exists(fname):
            extra_files.append(fname)

    if target.endswith("windows-msvc"):
        archive_file = f"build/{archive_name}.zip"
        with zipfile.ZipFile(archive_file, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(bin_path, bin_name)
            for f in extra_files:
                zf.write(f, os.path.basename(f))
        print(f"[+] Created {archive_file}")
    else:
        archive_file = f"build/{archive_name}.tar.gz"
        with tarfile.open(archive_file, "w:gz") as tf:
            tf.add(bin_path, bin_name)
            for f in extra_files:
                tf.add(f, os.path.basename(f))
        print(f"[+] Created {archive_file}")

def main():
    if host_only:
        build_target()
        return

    if system == "linux":
        tlist = targets["linux"]
        use_zig = True
    elif system == "darwin":
        tlist = targets["darwin"]
        use_zig = False
    elif system == "windows":
        tlist = targets["windows"]
        use_zig = False
    else:
        print(f"Unsupported system: {system}")
        sys.exit(1)

    install_targets(tlist)
    for t in tlist:
        build_target(t, use_zig)
        package_binary(version, t)

    print("All HOLG builds complete!")

if __name__ == "__main__":
    main()
