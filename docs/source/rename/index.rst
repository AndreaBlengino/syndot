rename
======

.. versionadded:: 2.0

Rename label in the :ref:`map file <map.ini>`.


Usage
-----

``syndot ([-o | --old] <OLD_LABEL>) ([-n | --new] <NEW_LABEL>) 
[[-m | --mapfile] <MAP_FILE>]``


Options
-------

* ``-h``, ``--help`` - Show the help message and exit.
* ``-m``, ``--mapfile`` ``<MAP_FILE>`` - Path to the :ref:`map file <map.ini>`. 
  If not provided search for a ``map.ini`` file in the current directory, so 
  not required if current directory is the settings directory.
* ``-n``, ``--new`` ``<NEW_LABEL>`` - New label to use
* ``-o``, ``--old`` ``<OLD_LABEL>`` - Existing label to rename
