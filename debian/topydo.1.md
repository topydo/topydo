% topydo(1)
%
% February 2021

# NAME

topydo -- An advanced todo.txt terminal utility for managing tasks

## SYNOPSIS

`topydo [-ahv] [-c <config>] [-C <colormode>] [-d <archive>]`
`       [-t <todo.txt>] subcommand [help|args]`

`topydo [--info]`

## DESCRIPTION

This is a command line tool for managing and displaying tasking information.

Tasks are stored in a plain text file using the todo.txt format. There are a
number of tools, across operating systems, that support collaboratively
managing a common tasking file.

## OPTIONS

_--info_
: Print out current configuration information for topydo, including the path
the executable and the tasking file.

_-a_
: Do not archive todo items on completion.

_-c_
: Specify an alternative configuration file.

_-C_
: Specify color mode (0 = disable, 1 = enable 16 colors,
16 = enable 16 colors, 256 = enable 256 colors, auto (default))

_-d_
: Specify an alternative archive file (done.txt)

_-h_
: This help text

_-t_
: Specify and alternative todo file

_-v_
: Print the version and exit

## BUILT-IN ACTIONS
Run "topydo help \<subcommand\> for additional help.

  * _add_|_a_ "THING I NEED TO DO +project @context"

    Adds THING I NEED TO DO to your todo.txt file on its own line.

    Project and context notation optional.

    Quotes optional.

  * _append_|_app_ ITEM# "TEXT TO APPEND"

    ```app ITEM# "TEXT TO APPEND"```

    Adds TEXT TO APPEND to the end of the task on line ITEM#.

    Quotes optional.

  * _del_|_rm_ ITEM# [TERM]

    Deletes the task on line ITEM# in todo.txt.

    If TERM specified, deletes only TERM from the task.

  * _depri_|_dp_ ITEM#[, ITEM#, ITEM#, ...]

    Deprioritizes (removes the priority) from the task(s)

    on line ITEM# in todo.txt.

  * _do_ ITEM#[, ITEM#, ITEM#, ...]

    Marks task(s) on line ITEM# as done in todo.txt.

  * _ls_ [TERM...]

    Displays all tasks that contain TERM(s) sorted by priority with line
    numbers.  Each task must match all TERM(s) (logical AND).
    Hides all tasks that contain TERM(s) preceded by a
    minus sign (i.e. -TERM). If no TERM specified, lists entire todo.txt.

  * _listcon_|_lscon_ [TERM...]

    Lists all the task contexts that start with the @ sign in todo.txt.
    If TERM specified, considers only tasks that contain TERM(s).

  * _listprojexts_|_lsprj_ [TERM...]

    Lists all the projects (terms that start with a + sign) in
    todo.txt.
    If TERM specified, considers only tasks that contain TERM(s).

  * _postpone_ ITEM#
    Postpone the task.

  * _pri_ ITEM# PRIORITY

    Adds PRIORITY to task on line ITEM#.  If the task is already
    prioritized, replaces current priority with new PRIORITY.
    PRIORITY must be a letter between A and Z.

  * _revert_ ITEM#

    Revert a previous task.


## TODO.TXT TASK FORMAT

A todo.txt task is a single line of text, which may contain specially notated
words to define metadata for the task. These tags are all optional.

  * (\<PRIORITY\>)

    A task _priority_ can be defined by prepending a single letter in
    parenthesis, followed by a space. By convention, capital letters are used,
    with 'A' denoting the highest priority.

  * +\<PROJECT\>

    A word in the task beginning with "+" defines the _project_ associated with
    the task. This provides a means to group tasks according to the tasks
    assocated with a particular effort.

  * @\<CONTEXT\>

    A word in the task beginning with the "@" character defines the _context_
    associated with the task. Possible contexts are @phone, @email, or @home.
    This provides a means to group tasks according to the context of when they
    can be completed.

  * due:\<yyyy-mm-dd\>

    Define the due date of the task.

  * x \<TASK\>

    A task may be marked complete by prepending an "x" followed by a space.
    This is used by the utility to remove tasks from active task lists without
    affecting the line numbers of the remaining tasks.

A task may also contain one or two bare dates that define the creation and
completion date of the task. A completed task should have the completion date
following the "x".

The core todo.txt format is described in full at
https://github.com/todotxt/todo.txt.

The format is extended by topydo with the following features:

  * rec:[+][n][d|w|m|y]

    Recur a task upon completion. The _+_ indicates strict recurrance, which
    bases the new date on the _due_ date. Otherwise, the closing date is
    used.

  * t:\<yyy-mm-dd>

    The threshold, or start date. Tasks with a threshold date in the future are
generally not shown.

## CONFIGURATION FILE

Configuration files may be stored in the following locations:

  * _/etc/topydo.conf_
  * _~/.config/topydo/config_
  * _~/.topydo_
  * _.topydo_ (in the current working directory)
  * _topydo.conf_ (in the current working directoy)
  * _topydo.ini_ (in the current working directoy)

The files are read in that order, with variables in later files overriding
earlier ones.

See the _Configuration_ topic in _/usr/share/doc/topydo/docs/index.html_ for
detail on the configuration file format and variables.

## SEE ALSO

todo.txt(1), topydo.conf(5), vitodo(1), edittodo(1), listtodo(1),
todo.txt-base(8)

The file _/usr/share/doc/topydo/docs/index.html_ contains extensive
information about _topydo_, including the configuration file format.
