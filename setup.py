from distutils.core import setup

setup(
    name = "Topydo",
    packages = ["topydo", "topydo.lib", "topydo.cli"],
    version = "0.1",
    description = "A todo list application using the todo.txt format.",
    author = "Bram Schoenmakers",
    author_email = "me@bramschoenmakers.nl",
    url = "https://github.com/bram85/topydo",
    download_url = "https://github.com/bram85/topydo/archive/master.zip",
)
