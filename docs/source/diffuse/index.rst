.. include:: ../substitutions.rst

diffuse
=======

Create dotfiles symlinks.


Usage
-----

``syndot diffuse ([[-l | --label] <LABEL>...] | [[-p | --path] <PATH>...]) 
[[-m | --mapfile] <MAP_FILE>] [[-s | --start] <PATH_START>] 
[-n | --no-confirm]``

Options
-------

* ``-h``, ``--help`` - Show the help message and exit.

* ``-l``, ``--label`` ``<LABEL> [<LABEL>...]`` - Label(s) to diffuse the 
  associated path(s). At least a ``<LABEL>`` or a ``<PATH>`` must be provided.

  .. versionadded:: 2.0

* ``-m``, ``--mapfile`` ``<MAP_FILE>`` - Path to the :ref:`map file <map.ini>`. 
  If not provided search for a ``map.ini`` file in the current directory, so 
  not required if current directory is the ``<SETTINGS>`` directory.

* ``-n``, ``--no-confirm`` - Do not ask for confirmation.

  .. versionadded :: 2.1

* ``-p``, ``--path`` ``<PATH> [<PATH>...]`` - Dotfile path(s) to diffuse. At 
  least a ``<LABEL>`` or a ``<PATH>`` must be provided.

  .. versionadded:: 2.0

* ``-s``, ``--start`` ``<PATH_START>`` - Filter target based on path starting 
  with <PATH_START>.

  .. versionadded:: 2.0
