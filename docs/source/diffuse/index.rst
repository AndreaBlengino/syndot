.. include:: ../substitutions.rst

diffuse
=======

Create dotfiles symlinks.


Usage
-----

``syndot diffuse [OPTION] [ARGUMENT]``


Arguments
---------

* ``TARGET_PATH`` - Dotfile path, mandatory if ``-a`` or ``--all`` option is not provided. Before diffusing a dotfile,
  it must be added to the :ref:`map file <map.ini>` beforehand with |command syndot add|.


Options
-------

* ``-a``, ``--all`` - Select all dotfiles in the :ref:`map file <map.ini>`, mandatory if ``<TARGET_PATH>`` argument is
  not provided.
* ``-e``, ``--exact`` - Search for an exact match for the ``<TARGET_PATH>`` argument in the :ref:`map file <map.ini>`.
  If not provided, search for all targets which paths begin with ``<TARGET_PATH>`` argument in the
  :ref:`map file <map.ini>`.
* ``-h``, ``--help`` - Show the help message and exit.
* ``-m``, ``--mapfile`` ``<MAP_FILE>`` - Path to the :ref:`map file <map.ini>`. If not provided search for a
  ``map.ini`` file in the current directory, so not required if current directory is the ``<SETTINGS>`` directory.
