from setuptools import setup

setup(
    name = "topydo",
    packages = ["topydo", "topydo.lib", "topydo.cli"],
    version = "0.3.2",
    description = "A command-line todo list application using the todo.txt format.",
    author = "Bram Schoenmakers",
    author_email = "me@bramschoenmakers.nl",
    url = "https://github.com/bram85/topydo",
    extras_require = {
        'ical': ['icalendar'],
        'edit-cmd-tests': ['mock'],
    },
    entry_points= {
        'console_scripts': ['topydo = topydo.cli.Main:main'],
    },
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
    ],
    long_description = """\
topydo is a todo list application using the todo.txt format. It is heavily inspired by the todo.txt CLI by Gina Trapani. This tool is actually a merge between the todo.txt CLI and a number of extensions that I wrote on top of the CLI. These extensions are:

* Set due and start dates;
* Custom sorting;
* Dealing with tags;
* Maintain dependencies between todo items;
* Allow todos to recur;
* Some conveniences when adding new items (e.g. adding creation date and use relative dates)
""",

    test_suite = "test",
)
