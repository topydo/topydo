topydo
======

topydo is a todo list application using the [todo.txt format][1]. It is heavily
inspired by the [todo.txt CLI][2] by Gina Trapani. This tool is actually a
merge between the todo.txt CLI and a [number of extensions][3] that I wrote
on top of the CLI, hereafter refered to as todo.txt-tools. These extensions
are:

* Set **due** and **start dates**;
* Custom sorting;
* Dealing with tags;
* Maintain **dependencies** between todo items;
* Allow todos to **recur**;
* Some conveniences when adding new items (e.g. adding creation date and use
  **relative dates**);

Consult the [wiki][4] for more information about the features and on how to
use topydo.

Motivation
----------

I rewrote the CLI from scratch for multiple reasons.

First, in the long term I'd like to write the perfect todo client. The perfect
todo client is free, open source, flexible and available wherever I am.
todo.txt is the perfect format, since it's simple and plain text and not bound
to a particular tool.

Second, the current (CLI) interface is handy, but has its limits when dealing
with large swaths of todo items. The CLI and a GUI should complement each
other.

Third, the original todo.txt CLI is a huge Bash script. In my opinion it's the
wrong language to write a serious application with it. It may behave
differently on other operating systems (or sometimes it's plain broken). The
todo.txt-tools that extend the CLI were (quickly) written in Perl. It doesn't
have a proper test suite and it sometimes doesn't play very well when a user
inputs something funny.

In order to achieve the long term vision of a perfect todo list, I need a solid
foundation in a solid language. Hence the rewrite in Python, sprinkeled with
unit tests.



[1]: https://github.com/ginatrapani/todo.txt-cli/wiki/The-Todo.txt-Format
[2]: https://github.com/ginatrapani/todo.txt-cli
[3]: https://github.com/bram85/todo.txt-tools
[4]: https://github.com/bram85/topydo/wiki
