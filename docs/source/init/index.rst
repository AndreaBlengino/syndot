.. _init:

init
====

Initialize the settings directory where store dotfiles.

Create the settings directory, if does not exist yet, and the default 
:ref:`map file <map.ini>` within it.


Usage
-----

``syndot init [[-p | --path] <PATH>]``


Options
-------

* ``-h``, ``--help`` - Show the help message and exit.
* ``-p``, ``--path`` ``<PATH>`` - Path to the settings directory. If not 
  provided, create the settings directory at the default path: ``~/Settings``.
