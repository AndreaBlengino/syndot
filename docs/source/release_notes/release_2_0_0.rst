.. include:: substitutions.rst

*************
Version 2.0.0
*************


New Features
------------

* Grouping of target paths into labels


API Changes
-----------

* Add ``-l``, ``--label`` option to |add|, |diffuse|, |link|, |list|, |remove| 
  and |unlink| commands to handle labels

* Add ``-p``, ``--path`` option to |add|, |diffuse|, |link|, |list|, |remove| 
  and |unlink| commands to handle target paths

* Add ``-d``, ``--directory`` option to |list| command to print settings 
  directory

* Add ``-s``, ``--start`` option to |diffuse|, |link| and |unlink| commands to 
  filter target based on path starting

* Add ``rename`` command to rename existing labels in the 
  :ref:`map file <map.ini>`

* Remove ``-a``, ``--all`` option from |diffuse|, |link| and |unlink| commands

* Remove ``-e``, ``--exact`` option from |diffuse|, |link| and |unlink| commands

* Remove ``TARGET_PATH`` argument from |add|, |diffuse|, |link|, |remove| and 
  |unlink| commands


Enhancements
------------

* Fix Python syntax according to `PEP 8 <https://peps.python.org/pep-0008>`_

* Move log file to ``~./local/share/syndot`` directory

* Change default color scheme

