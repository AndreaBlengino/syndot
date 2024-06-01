.. _init:

init
====

Initialize ``<SETTINGS>`` directory where store dotfiles.

Create the ``<SETTINGS>`` directory, if does not exist yet, and the default :ref:`map file <map.ini>` within it.


Usage
-----

``syndot init [OPTION]``


Options
-------

* ``-h``, ``--help`` - Show the help message and exit.
* ``-p``, ``--path`` - Path to the ``<SETTINGS>`` directory. If not provided, create the ``<SETTINGS>`` directory at
  the default path: ``~/Settings``.
