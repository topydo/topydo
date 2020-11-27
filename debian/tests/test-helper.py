#!/usr/bin/python3

import os
import sys
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

cp = run(["topydo", "--info"], capture_output=True, encoding="utf-8")
passed = False
for line in cp.stdout.split("\n"):
    if line == "task_path = /tmp/todo.txt":
        passed = True

with open(str(artifact_path / "todo.txt-helper-config.txt"), "w") as fp:
    fp.write(cp.stdout)

config_path.unlink()

os.chdir(str(start_path))

if not passed:
    print("Did not find task file path")

    sys.exit(1)
