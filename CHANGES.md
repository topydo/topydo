0.9
---

* Dropped support for Python 2.7.
* Add ability to filter on creation/completion dates:

        topydo ls created:today
        topydo ls completed:today
        topydo -t done.txt completed:today # if auto-archiving is set

* `ls -F` supports `%P` that expands to a single space when no priority is set,
  in contrast to `%p` which expands to an empty string (thanks to @MinchinWeb).
* `ls -N` prints enough todo items such that it fits on one screen (thanks to
  @MinchinWeb).
* Aliases can have a `{}` placeholder which is substituted with the alias'
  arguments (thanks to @mruwek).
* `pri` accepts priorities in lowercase (thanks to @MinchinWeb).
* Several bugfixes for `dep gc`.
* Various test/CI improvements.

0.8
---

* `do -d` understands relative dates.

* Introduced `yesterday` as a relative date (abbrev. `yes`).

* `tag` command understands relative dates when setting due or t tags.

* Fix install of wheels (unnecessarily installed dependencies). Issue #79.

* Bugfix: the negation of ordinal tag filters did not work.

* Some improvements in test coverage (a.o. thanks to @mruwek).

0.7
---

A big release with many new features. Many thanks to Jacek Sowiński (@mruwek)
for the majority of these new features.

* `ls` output can be customized with a -F flag or a configuration option:

        [ls]
        list_format = |%I| %x %{(}p{)} %c %s %k %{due:}d %{t:}t

  or `ls -F "%{(}p{)} %s %{due:}d"`.

  See `help ls` for all placeholders. Each placeholder can optionally be
  surrounded by optional texts that are only printed when the placeholder is
  expanded to a value.

  The format string may contain a tab character: all text that follows is
  aligned to the right.

  (thanks to @mruwek)
* New subcommand: `revert`. Revert the last executed command(s). The number of
  revisions can be tuned in the configuration file:

      [topydo]
      backup_count = 25

  Set to 0 to disable this feature. (thanks to @mruwek)
* New feature: aliases. Aliases can be defined in the configuration file:

        [aliases]
        showall = ls -x

  (thanks to @mruwek)
* Filter based on priorities (thanks to @mruwek)

      ls (A)
      ls (<A)

* `ls` has a `-n` flag to limit the number of todo items (similar to the
  list_limit option in the configuration file:

      ls -n 5

* `ls` has a `-i` flag to select displaying todo items based on their ID. This
  can be useful to have a 'clean' default view, and to gather more details for
  a certain todo item using aliases and formatting.
* Prompt mode no longer warns about background modifications to todo.txt when a
  read-only command is entered (e.g. `ls`).
* Removed restriction in `edit` mode that requires keeping the same amount of
  lines in the todo.txt file.
* `edit` only processes the todo items when edits were actually made in the
  editor (thanks to @mruwek)
* When entering today's day of the week as a relative date, it will use next
  week's date instead of today.
* Bugfix: not all tags were properly hidden with the `hide_tags` configuration
  option.
* Better PEP8 compliance (thanks to @MinchinWeb)
* Various test/CI improvements (thanks to @MinchinWeb)
* Support for Python 3.2 removed.
* Many other minor improvements (a.o. thanks to @MinchinWeb)

0.6
---

* Recurrence patterns can be prefixed with a `+` to indicate strict recurrence
  (i.e. based on due date rather than completion date. This syntax is inspired
  from the SimpleTask project by @mpcjanssen.
* Colors now work on the Windows commandline (thanks to @MinchinWeb). Requires
  colorama to be installed.
* Do not print spurious color codes when colors are disabled in the
  configuration (thanks to @MinchinWeb).
* In prompt mode, restore old auto-completion behavior: press Tab for
  completion (instead of complete while typing).
* Various other minor fixes (thanks to @MinchinWeb).

0.5
---

* Remove 'ical' subcommand in favor of 'topydo ls -f ical'
* Remove options highlight_projects_colors in favor of colorscheme options. In
  case you wish to disable the project/context colors, assign an empty value in
  the configuration file:

      [colorscheme]
      project_color =
      context_color =
* `del`, `depri`, `do`, `pri`, `postpone` now support now expression like `ls`
  does, using the `-e` flag (Jacek Sowiński, @mruwek).
* Fix `ls` when searching for a certain key:value where value is a string.
* Disable auto archive when the option archive_filename is empty.
* Add option auto_creation_date to enable/disable the creation date being added
  to new todo items.
* Calculate relative dates correctly in long-running `prompt` sessions.
* `pri` also accepts priorities in the form (A), [A] or any other bracket.
* Add `listcontext` and `listcontexts` as aliases of `lscon`.
* Highlight tags when the value is one character long.
* Cleanups

0.4.1
-----

* Fix infinite loop when `keep_sorted` is enabled in the configuration.
* Depend on prompt-toolkit >= 0.39, which fixes the history functionality in
  prompt mode (up/down keys).

0.4
---

* A new prompt mode with autocompletion. To enable, run `pip install
  prompt-toolkit`, then `topydo prompt`.
* Support for Python 3.2, 3.3 and 3.4 (note that iCalendar output does not
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
