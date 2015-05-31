0.4
---

* A new prompt mode with autocompletion. To enable, run `pip install
  prompt-toolkit`, then `topydo prompt`.
* Support for Python 3.2, 3.3 and 3.4 (note that the `ical` subcommand does not
  work in Python 3.2)
* Better Unicode support.
* `add` command has the `-f` flag to add todo items from a file (or use `-` to
  read from standard input) (Jacek Sowiński - @mruwek)
* Customizable colors + additional highlighting of tags and URLs (Jacek
  Sowiński (@mruwek) and @kidpixo).
* Make sure that the `edit` subcommand always uses the correct todo.txt file.
* `ls` subcommand has the `-f` flag to specify the output format. Currently,
  three formats are supported:
  * `text` - The default plain text format.
  * `ical` - iCalendar (WARNING: this deprecates the `ical` subcommand)
  * `json` - Javascript Object Notation (JSON)
* Resolve `~` to home directory if used in a configuration file
  (@robertvanbregt).
* Various minor fixes.

Again, I'd like to thank Jacek (@mruwek) for his assistance and contributions
in this release.

0.3
---

* `edit` subcommand accepts a list of numbers or an expression to select which
  items to edit. (Jacek Sowiński)
* The commands `del`, `do`, `pri`, `depri` and `postpone` can operate on multiple
  todo items at once. (Jacek Sowiński)
* A new `ical` subcommand that outputs in the iCalendar format.
* New configuration option: `append_parent_contexts`. Similar to
  `append_parent_projects` where the parent's contexts are automatically added
  to child todo items. (Jacek Sowiński)
* New configuration option: `hide_tags` to hide certain tags from the `ls`
  output. Multiple tags can be specified separated by commas. By default, `p`,
  `id` and `ical` are hidden.
* Properly complete todo items with invalid recurrence patterns (`rec` tag).
* Fix assignment of dependency IDs: in some cases two distinct todos get the
  same dependency ID.

Big thanks to Jacek (@mruwek) for his contributions in this release.

0.2
---

* A new `edit` subcommand to launch an editor with the configured todo.txt file.
* Introduced textual identifiers in addition to line numbers.

  Line numbers are still the default, textual identifiers can be enabled with
  the option `identifiers = text` in the configuration file (see topydo.conf).
  The advantage of these identifiers is that they are less prone to changes when
  something changes in the todo.txt file. For example, identifiers are much more
  likely to remain the same when completing a todo item (and archiving it). With
  linenumbers, all todo items below the completed one would get a new
  identifier.
* Relative dates with months and years are more accurate now (thanks to Jacek
  Sowiński).
* Multiple items can be marked as complete or deleted at once.
* Added option to automatically add the projects of the parent todo item when
  adding a child todo item. Enable `append_parent_projects` in topydo.conf.
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
