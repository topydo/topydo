from setuptools import setup, find_packages
import os
import re
import codecs
import sys

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^VERSION = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name = "topydo",
    packages = find_packages(exclude=["test"]),
    version = find_version('topydo', 'lib', 'Version.py'),
    description = "A powerful todo.txt application for the console",
    author = "Bram Schoenmakers",
    author_email = "bram@topydo.org",
    url = "https://www.topydo.org",
    install_requires = [
        'arrow >= 0.7.0',
    ],
    extras_require = {
        ':sys_platform=="win32"': ['colorama>=0.2.5'],
        ':python_version=="3.2"': ['backports.shutil_get_terminal_size>=1.0.0'],
        'columns': ['urwid >= 1.3.0'],
        'ical': ['icalendar'],
        'prompt': ['prompt_toolkit >= 0.53'],
        'test': ['coverage', 'freezegun', 'green', ],
        'test:python_version=="3.2"': ['mock'],
    },
    entry_points= {
        'console_scripts': ['topydo = topydo.ui.UILoader:main'],
    },
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Utilities",
    ],
    long_description = """\
topydo is a powerful and customizable todo.txt application for the console, inspired by the todo.txt CLI by Gina Trapani.

Highlights of the additional features it provides:

* Set due and start dates;
* Multiple UIs (CLI, prompt and a column-based TUI);
* Custom sorting;
* Manage tags;
* Maintain dependencies between todo items;
* Allow todos to recur;
* Some conveniences when adding new items (e.g. adding creation date and use relative dates)
""",

    test_suite = "test",
)
