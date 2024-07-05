list
====

List dotfiles in the :ref:`map file <map.ini>`.


Usage
-----

``syndot list [-d | --directory] [[-l | --label] | [-p | --path]] 
[[-m | --mapfile] <MAP_FILE>]``


Options
-------

* ``-d``, ``--directory`` - Print the settings directory
* ``-h``, ``--help`` - Show the help message and exit.
* ``-l``, ``--label`` - List only target labels. Not allowed together with the 
  ``[-p | --path]`` option
* ``-m``, ``--mapfile`` ``<MAP_FILE>`` - Path to the :ref:`map file <map.ini>`. 
  If not provided search for a ``map.ini`` file in the current directory, so 
  not required if current directory is the settings directory.
* ``-p``, ``--path`` - List only target paths. Now allowed together with the 
  ``[-l | --label]`` option
