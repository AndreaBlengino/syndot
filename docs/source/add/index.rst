add
===

Add dotfiles to the :ref:`map file <map.ini>`.

Dotfile paths are grouped together in labels.


Usage
-----

``syndot add ([-l | --label] <LABEL>) ([-p | --path] <PATH>...) 
[[-m | --mapfile] <MAP_FILE>]``


Options
-------

* ``-h``, ``--help`` - Show the help message and exit.

* ``-l``, ``--label`` ``<LABEL>`` - Label under which to group multiple target 
  paths relating to the same set of configurations. A single label must be 
  provided.
  
  .. versionadded:: 2.0

* ``-m``, ``--mapfile`` ``<MAP_FILE>`` - Path to the :ref:`map file <map.ini>`.
  If not provided search for a ``map.ini`` file in the current directory, so 
  not required if current directory is the settings directory.

* ``-p``, ``--path`` ``<PATH> [<PATH>...]`` - Dotfile path(s) to be added to 
  the map file and grouped under ``<LABEL>``. At least a path must be provided.

  .. versionadded:: 2.0
