% topydo.conf(5)
%
% November 2020

# NAME

topydo.conf -- Configuration files for topydo

## DESCRIPTION

The _topydo_ command will attempt to read configuration file information from
the following locations:

  • _/etc/topydo.conf_
  • _~/.config/topydo/config_
  • _~/.topydo_
  • _.topydo_ (in the current working directory)
  • _topydo.conf_ (in the current working directoy)
  • _topydo.ini_ (in the current working directoy)

The files are read in that order, with variables in later files overriding
earlier ones.

The configuration sections and variables are documented in _/etc/topydo.conf_
and _/usr/share/doc/topydo/Documentation.html_.

## SEE ALSO

todo.txt(1), vitodo(1), edittodo(1), listtodo(1), todo.txt-base(8)
