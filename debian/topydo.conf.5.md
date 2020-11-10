% topydo.conf(5)
%
% November 2020

# NAME

topydo.conf -- Configuration files for topydo

## DESCRIPTION

The _topydo_ command will attempt to read configuration file information from the following locations:

  • _/etc/topydo.conf_
  • _~/.config/topydo/config_
  • _~/.topydo_
  • _.topydo_ (in the current working directory)
  • _topydo.conf_ (in the current working directoy)
  • _topydo.ini_ (in the current working directoy)

The files are read in that order, with variables in later files overriding earlier ones.

The configuration sections and variables are documented in _/etc/topydo.conf_
and _/usr/share/doc/topydo/Documentation.html_.

## SEE ALSO

todo.txt-helper(8), todo(8), todo.txt(8), vitodo(8), edittodo(8), listtodo(8)
