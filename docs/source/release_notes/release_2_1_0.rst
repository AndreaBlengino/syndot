.. include:: substitutions.rst

*************
Version 2.1.0
*************


New Features
------------

* Add ``-n``, ``--no-confirm`` option to |diffuse|, |link| and |unlink| 
  commands to avoid confirmation request

* Add ``-i``, ``--interactive`` option to |diffuse|, |link| and |unlink| 
  commands to select labels in interactive mode using gum_, if it is installed 
  in the system

* Add gum_ support in confirmation prompt for |diffuse|, |link| and |unlink| 
  commands

* Add ``-s``, ``-search`` option to |list| to list path(s) of a searched label


Enhancements
------------

* |rename| groups labels if the ``-n``, ``--new`` ``label`` is already in the 
  :ref:`map file <map.ini>`

* |add| checks if the path to be added is already listed in other labels before 
  adding it to the :ref:`map file <map.ini>`, in order to keep only unique paths

* Enhanced color scheme management

* Update dependencies for documentation and testing

