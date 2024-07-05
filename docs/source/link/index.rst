.. include:: ../substitutions.rst

link
====

Move dotfiles to the settings directory and create symlinks to them.


Usage
-----

``syndot link [-b | --backup] ([[-l | --label] <LABEL>...] | 
[[-p | --path] <PATH>...]) [[-m | --mapfile] <MAP_FILE>]``


Options
-------

* ``-b``, ``--backup`` - Create a backup copy of the original dotfile.
* ``-h``, ``--help`` - Show the help message and exit.
* ``-l``, ``--label`` ``<LABEL> [<LABEL>...]`` - Label(s) to link the 
  associated path(s). At least a ``<LABEL>`` or a ``<PATH>`` must be provided
* ``-m``, ``--mapfile`` ``<MAP_FILE>`` - Path to the :ref:`map file <map.ini>`. 
  If not provided search for a ``map.ini`` file in the current directory, so 
  not required if current directory is the settings directory.
* ``-p``, ``--path`` ``<PATH> [<PATH>...]`` - Dotfile path(s) to link. At 
  least a ``<LABEL>`` or a ``<PATH>`` must be provided
