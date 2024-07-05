.. include:: ../substitutions.rst

unlink
======

Remove symlinks and move dotfiles from settings directory to their original 
directories.


Usage
-----

``syndot unlink ([[-l | --label] <LABEL>...] | [[-p | --path] <PATH>...]) 
[[-m | --mapfile] <MAP_FILE>]``


Options
-------

* ``-h``, ``--help`` - Show the help message and exit.
* ``-l``, ``--label`` ``<LABEL> [<LABEL>...]`` - Label(s) to unlink the 
  associated path(s). At least a ``<LABEL>`` or a ``<PATH>`` must be provided
* ``-m``, ``--mapfile`` ``<MAP_FILE>`` - Path to the :ref:`map file <map.ini>`. 
  If not provided search for a ``map.ini`` file in the current directory, so 
  not required if current directory is the settings directory.
* ``-p``, ``--path`` ``<PATH> [<PATH>...]`` - Dotfile path(s) to unlink. At 
  least a ``<LABEL>`` or a ``<PATH>`` must be provided
