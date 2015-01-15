0.2
---

(unreleased)

* A new 'edit' subcommand to launch an editor.
* Introduced textual identifiers in addition to line numbers.

  Line numbers are still the default, textual identifiers can be enabled with
  the option 'identifiers = text' in the configuration file (see topydo.conf).
  The advantage of these identifiers is that they are less prone to changes when
  something changes in the todo.txt file. For example, identifiers are much more
  likely to remain the same when completing a todo item (and archiving it). With
  linenumbers, all todo items below the completed one would get a new
  identifier.
* Relative dates with months and years are more accurate now (thanks to Jacek
  Sowiński).
* Multiple items can be marked as complete or deleted at once.
* Added option to automatically add the projects of the parent todo item when
  adding a child todo item. Enable append_parent_projects in topydo.conf.
* `topydo help` shows a list of available subcommands. Moreover, you can run
  `topydo help <subcommand>` as well.
* Let setuptools provide a `topydo` executable.
* Various other fixes.

0.1.2
-----

* Handle recurrence properly when a custom completion date is given.
* Allow any tag to have a date value (so it can be filtered as such).

0.1.1
-----

* Write newline character at the end of todo.txt and done.txt files.
* Tag values must be at least one character long.
* Made filtering a bit more robust w.r.t. integer expressions.

0.1
---

Initial release.
