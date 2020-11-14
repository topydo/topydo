#!/usr/bin/python3

import os
from pathlib import Path
from subprocess import run

WORKDIR = "/tmp"
work_path = Path(WORKDIR)

if "AUTOPKGTEST_ARTIFACTS" in os.environ:
    artifact_path = Path(os.environ["AUTOPKGTEST_ARTIFACTS"])
else:
    artifact_path = work_path

config_path = work_path / "topydo.conf"

start_path = Path(os.getcwd())
os.chdir(WORKDIR)

if config_path.exists():
    config_path.unlink()

with open(str(config_path), "w") as fp:
    fp.write("[topydo]\n")
    fp.write("filename = /tmp/todo.txt\n")

cp = run(["todo.txt-helper"], capture_output=True, encoding="utf-8")
assert cp.stdout.strip() == "/tmp/todo.txt"
with open(str(artifact_path / "todo.txt-helper-config.txt"), "w") as fp:
    fp.write(cp.stdout)

config_path.unlink()

os.chdir(str(start_path))
