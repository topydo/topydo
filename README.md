topydo
======

[![Build Status](https://travis-ci.org/bram85/topydo.svg?branch=master)](https://travis-ci.org/bram85/topydo) [![Join the chat at https://gitter.im/bram85/topydo](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/bram85/topydo?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) [![Flattr this git repo](http://api.flattr.com/button/flattr-badge-large.png)](https://flattr.com/submit/auto?user_id=bram85&url=https://github.com/bram85/topydo&title=topydo&language=&tags=github&category=software) 

topydo is a todo list application using the [todo.txt format][1]. It is heavily
inspired by the [todo.txt CLI][2] by Gina Trapani. This tool is actually a
merge between the todo.txt CLI and a [number of extensions][3] that I wrote
on top of the CLI. These extensions are:

* Set **due** and **start dates**;
* Custom sorting;
* Dealing with tags;
* Maintain **dependencies** between todo items;
* Allow todo items to **recur**;
* Some conveniences when adding new items (e.g. adding creation date and use
  **relative dates**);

Consult the [wiki][4] for more information about the features and on how to
use topydo.

Install
-------

Simply install with:

    pip install topydo

### Optional dependencies

* [icalendar][7]      : To print your todo.txt file as an iCalendar file
                        (not supported for Python 3.2).
* [prompt-toolkit][6] : For topydo's _prompt_ mode, which offers a shell-like
                        interface with auto-completion.

Demo
----

![gif][5]


[1]: https://github.com/ginatrapani/todo.txt-cli/wiki/The-Todo.txt-Format
[2]: https://github.com/ginatrapani/todo.txt-cli
[3]: https://github.com/bram85/todo.txt-tools
[4]: https://github.com/bram85/topydo/wiki
[5]: https://raw.githubusercontent.com/bram85/topydo/master/doc/topydo.gif
[6]: https://github.com/jonathanslenders/python-prompt-toolkit
[7]: https://github.com/collective/icalendar
