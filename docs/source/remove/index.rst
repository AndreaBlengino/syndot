remove
======

Remove dotfiles from the :ref:`map file <map.ini>`.


Usage
-----

``syndot remove ([[-l | --label] <LABEL>...] | [[-p | --path] <PATH>...]) 
[[-m | --mapfile] <MAP_FILE>]``


Options
-------

* ``-h``, ``--help`` - Show the help message and exit.

* ``-l``, ``--label`` ``<LABEL> [<LABEL>...]`` - Label(s) and relative path(s) 
  to remove from the map file. One or more labels can be provided. At least a 
  ``<LABEL>`` or a ``<PATH>`` must be provided.

  .. versionadded:: 2.0

* ``-m``, ``--mapfile`` ``<MAP_FILE>`` - Path to the :ref:`map file <map.ini>`. 
  If not provided search for a ``map.ini`` file in the current directory, so 
  not required if current directory is the settings directory.

* ``-p``, ``--path`` ``<PATH> [<PATH>...]`` - Dotfile path(s) to remove from 
  the map file. One of more paths can be provided. At least a ``<LABEL>`` or a 
  ``<PATH>`` must be provided.

  .. versionadded:: 2.0
