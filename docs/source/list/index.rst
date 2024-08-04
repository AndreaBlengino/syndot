list
====

List dotfiles in the :ref:`map file <map.ini>`.


Usage
-----

``syndot list [-d | --directory] [[-l | --label] | [-p | --path] | 
[[-s | --search] <SEARCH>]] [[-m | --mapfile] <MAP_FILE>]``


Options
-------

* ``-d``, ``--directory`` - Print the settings directory.

  .. versionadded:: 2.0

* ``-h``, ``--help`` - Show the help message and exit.

* ``-l``, ``--label`` - List only target labels. Not allowed together with the 
  ``[-p | --path]`` or ``[-s | --search]`` options.

  .. versionadded:: 2.0

* ``-m``, ``--mapfile`` ``<MAP_FILE>`` - Path to the :ref:`map file <map.ini>`. 
  If not provided search for a ``map.ini`` file in the current directory, so 
  not required if current directory is the settings directory.

* ``-p``, ``--path`` - List only target paths. Now allowed together with the 
  ``[-l | --label]`` or ``[-s | --search]`` options.

  .. versionadded:: 2.0

* ``-s``, ``--search`` ``<SEARCH>`` - List paths of the specified ``<SEARCH>``
  label. Not allowed together with the ``[-l | --label]`` or ``[-p | --path]`` 
  options

  .. versionadded :: 2.1
