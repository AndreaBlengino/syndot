.. include:: ../substitutions.rst

unlink
======

Remove symlinks and move dotfiles from settings directory to their original 
directories.

Interactive mode to select label(s) is available only if gum_ is installed in 
the system.

Usage
-----

``syndot unlink ([-i | --interactive] | [[-l | --label] <LABEL>...] | 
[[-p | --path] <PATH>...]) [[-m | --mapfile] <MAP_FILE>] [-n | --no-confirm] 
[[-s | --start] <PATH_START>]``


Options
-------

* ``-h``, ``--help`` - Show the help message and exit.

* ``-i``, ``--interactive`` - Select label(s) to unlink the associated path(s) 
  in interactive mode using gum_, if it is installed in the system. At least a 
  label must be selected. Not allowed together with ``[-l | --label]`` or 
  ``[-p | --path]`` options.

  .. versionadded :: 2.1

* ``-l``, ``--label`` ``<LABEL> [<LABEL>...]`` - Label(s) to unlink the 
  associated path(s). At least a ``<LABEL>`` must be provided. Not allowed 
  together with ``[-i | --interactive]`` or ``[-p | --path]`` options.

  .. versionadded:: 2.0

* ``-m``, ``--mapfile`` ``<MAP_FILE>`` - Path to the :ref:`map file <map.ini>`. 
  If not provided search for a ``map.ini`` file in the current directory, so 
  not required if current directory is the settings directory.

* ``-n``, ``--no-confirm`` - Do not ask for confirmation.

  .. versionadded :: 2.1

* ``-p``, ``--path`` ``<PATH> [<PATH>...]`` - Dotfile path(s) to unlink. At 
  least a ``<PATH>`` must be provided. Not allowed together with 
  ``[-i | --interactive]`` or ``[-l | --label]`` options.

  .. versionadded:: 2.0


* ``-s``, ``--start`` ``<PATH_START>`` - Filter target based on path starting 
  with ``<PATH_START>``.

  .. versionadded:: 2.0
