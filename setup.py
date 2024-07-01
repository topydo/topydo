import codecs
import os
import re
from pathlib import Path

from setuptools import find_packages, setup

_HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(_HERE, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^VERSION = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

def long_description():
    path = Path(__file__).parent / "README.md"
    return path.read_text()

WATCHDOG = 'watchdog >= 0.8.3'
ICALENDAR = 'icalendar'

setup(
    name="topydo",
    packages=find_packages(exclude=["test"]),
    version=find_version('topydo', 'lib', 'Version.py'),
    description="A powerful todo.txt application for the console",
    author="Bram Schoenmakers",
    author_email="bram@topydo.org",
    url="https://github.com/topydo/topydo",
    install_requires=[
        'arrow >= 0.7.0',
    ],
    tests_require=[
        'freezegun',
    ],
    extras_require={
        ':sys_platform=="win32"': ['colorama>=0.2.5'],
        'columns': ['urwid >= 1.3.0', WATCHDOG],
        'ical': [ICALENDAR],
        'prompt': ['prompt_toolkit >= 0.53', WATCHDOG],
        'test': ['coverage>=4.3', 'freezegun', 'green', ICALENDAR, 'pylint>=1.7.1'],
    },
    entry_points={
        'console_scripts': ['topydo=topydo.ui.UILoader:main'],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Utilities",
    ],
    long_description=long_description(),
    long_description_content_type="text/markdown",
    test_suite="test",
)
