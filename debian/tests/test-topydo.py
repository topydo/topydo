#!/usr/bin/python3

import os
from pathlib import Path
from subprocess import run

# Set up paths
WORKDIR = "/tmp"
work_path = Path(WORKDIR)

if "AUTOPKGTEST_ARTIFACTS" in os.environ:
    artifact_path = Path(os.environ["AUTOPKGTEST_ARTIFACTS"])
else:
    artifact_path = work_path

config_path = work_path / "topydo.conf"
todo_path = artifact_path / "todo.txt"

start_path = Path(os.getcwd())
os.chdir(WORKDIR)

if config_path.exists():
    config_path.unlink()

if todo_path.exists():
    todo_path.unlink()

# Set up config
with open(str(config_path), "w") as fp:
    fp.write("[topydo]\n")
    fp.write("filename = %s\n" % str(todo_path))

# Can I add a tasks using topydo?
run("topydo add Foo".split(), capture_output=True, encoding="utf-8")
with open(str(todo_path), "r") as fp:
    todo_txt = fp.read()
assert "Foo" in todo_txt

# Can I list that task using todo?
cp = run("todo ls".split(), capture_output=True, encoding="utf-8")
assert "Foo" in cp.stdout

config_path.unlink()
todo_path.unlink()
(todo_path.parent / ".todo.bak").unlink()

os.chdir(str(start_path))
