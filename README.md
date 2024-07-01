topydo - a powerful todo.txt application
========================================

[![Build Status](https://travis-ci.org/topydo/topydo.svg?branch=master)](https://travis-ci.org/topydo/topydo) [![codecov.io](https://codecov.io/github/topydo/topydo/coverage.svg?branch=master)](https://codecov.io/github/topydo/topydo?branch=master) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/2957b80fffa0460bbb0e1ff7948f0ee7)](https://www.codacy.com/app/bram85/topydo?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=bram85/topydo&amp;utm_campaign=Badge_Grade) [![PyPI version](https://badge.fury.io/py/topydo.svg)](https://badge.fury.io/py/topydo)

topydo is a powerful todo list application using the [todo.txt format][1].

It has three user interfaces:

* Command Line Interface (CLI) - originally inspired by the [todo.txt CLI][2]
  by Gina Trapani.
* Prompt mode - a convenience mode for the CLI. Launch with `topydo prompt`.
* Column mode - a text based user interface (TUI) with customizable columns and
  vim-like bindings. Launch with `topydo columns`.

![png][6]

Features
--------

Feature-wise, the todo.txt format is quite limited, but can be extended using
tags. topydo natively supports some of these tags to implement:

* **Due** and **start dates**;
* Maintain **dependencies** between todo items;
* **recurring** todo items;

topydo also offers:

* Fine-grained control on **sorting** and **grouping** items;
* Customizable output;
* Some conveniences when adding new items (e.g. adding creation date and use
  **relative dates**);
* Additional output formats to iCalendar, JSON and Graphviz Dot;
* Aliases for frequently used commands.
* Text based todo identifiers, which are more stable and convenient than
  line-based todo identifiers.

Yet, topydo is fully todo.txt compliant. The text file can be processed by
other todo.txt tools (but they may not interpret the tags properly).

The documentation on [the TiddlyWiki][4] provides more information about the
features and how to use topydo.

Installation
------------

Simply install with:

    pip3 install topydo

If you wish to use column mode: install additional dependencies with:

    pip3 install topydo[columns]

Similarly, for prompt mode you can install additional dependencies with:

    pip3 install topydo[prompt]

Demo
----

CLI mode:

![gif][5]

[1]: https://github.com/ginatrapani/todo.txt-cli/wiki/The-Todo.txt-Format
[2]: https://github.com/ginatrapani/todo.txt-cli
[3]: https://github.com/bram85/todo.txt-tools
[4]: https://topydo.org/
[5]: https://raw.githubusercontent.com/topydo/topydo/master/docs/topydo.gif
[6]: https://raw.githubusercontent.com/topydo/topydo/master/docs/columns.png
