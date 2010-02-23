Developer Guidelines
####################

.. sidebar:: Summary

    :Release: |release|
    :Date: |today|
    :Authors: **Thomas Cokelaer**
    :Target: developers and administrators
    :status: mature


.. topic:: Overview

    This page is dedicated to developers guide lines

.. note:: When committing significant changes or fix bug, please update the Changelog.txt of the package(s) concerned.


Coding rules
=============

* Always use English language in your commentaries.
* 80-characters width.
* No tabs, use spaces
* indentations are 4 spaces
* Separate words in names with underscores.
* No mention of type in the variable name, especially no Hungarian notation.
* No abbreviations in names.
* If you work on existing code, respect the existing format.






Why using spaces instead of tabs
================================

tabs drawbacks
--------------
  * people mix tabs and spaces without knowing it or taking care of it.
  * people may use tabs for spaces (e.g., in strings)
  * copy and paste does not always keep the indentation, mix of tabs and spaces causes syntax errors

tabs advantages
---------------
  * avoid to type a lot of spaces BUT most of the editors have options to replace the effect of pressing the tab key by the relevant number of spaces.
  * people can dynamically change the indentation.

We decided to use spaces instead of tabs as much as possible.
