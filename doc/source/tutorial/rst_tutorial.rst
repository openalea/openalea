.. _rst_tutorial:

################################
Restructured Text quick overview
################################

This section is a brief introduction to reStructuredText (reST) concepts
 and syntax. It is intended to provide information and material to authors who 
 wishes to document their Python code (either in the DocString, or within an 
 independant reST file). The content of this page is based on more detailled 
 documentation found at: 

* `Sphinx reST documentation <http://sphinx.pocoo.org/rest.html>`_
* `Docutils rst documentation <http://docutils.sourceforge.net/rst.html>`_  

Here is a also a few hints on sphinx  :ref:`sphinx_tutorial`.

Introduction
============

	
reStructuredText is an easy-to-read, what-you-see-is-what-you-get plaintext
markup syntax and parser system. It is useful for in-line program documentation
(such as Python docstrings), for quickly creating simple web pages, and for
standalone documents. Here is an example provided in `Docutils rst documentation 
<http://docutils.sourceforge.net/rst.html>`_, which can be useful to start with.

 
.. seealso:: `<http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_

.. warning::
	reST syntax is sensitive to indentation !

.. warning::
	reST requires blank lines between paragraphs

Text, Inline markup
===================

The standard reST inline markup uses:

* one asterisk: ``*text*`` for emphasis (italics),
* two asterisks:``**text**`` for strong emphasis (boldface), and
* backquotes: ````text```` for code samples.
* single backquotes: ```text``` for reST special commands (e.g., hyper 
  links with spaces).

If asterisks or backquotes appear in running text and could be confused 
with inline markup delimiters, they have to be escaped with a backslash.

Be aware of some restrictions of this markup:

* it may not be nested,
* content may not start or end with whitespace: ``* text*`` is wrong,
* it must be separated from surrounding text by non-word characters. 

Use a backslash escaped space to work around that:

* ``this is a *longish* paragraph`` is correct and gives *longish*.
* ``this is a long*ish* paragraph`` is not interpreted as expected. You 
  should use ``this is a long\ *ish* paragraph`` to obtain long\ *ish* paragraph
    
.. warning::
    In Python strings it will, of course, be necessary to escape any backslash
    characters so that they actually reach reStructuredText. The simplest 
    way to do this is to use raw strings:

    ===================================== =======================
    Python string                         Typical result
    ===================================== =======================
    ``r"""\*escape* \`with` "\\""""``     ``*escape* `with` "\"``
    ``"""\\*escape* \\`with` "\\\\""""``  ``*escape* `with` "\"``
    ``"""\*escape* \`with` "\\""""``      ``escape with ""``
    ===================================== =======================     
    
    
Section
=======
Writing heading is as simple as::

    *****
    Title
    *****
    subtitle
    ########
    subsubtitle
    ***********
    and so on

Normally, there are no heading levels assigned to certain characters as the 
structure is determined from the succession of headings. However, for the 
Python documentation, this convention is used which you may follow:

* `#` with overline, for parts
* `*` with overline, for chapters
* `=`, for sections
* `-`, for subsections
* `^`, for subsubsections
* `"`, for paragraphs

Links
=====
There are two ways to define a link. First, by defining an alias at the end of 
your reST document::

    .. _Python: http://www.python.org/

Then, write your text inserting the keywrod ``Python_`` . The final
 result will be as follows:: Python_ .
 
.. note::
    Note that when you define the reference or alias, the underscore is before
    the keyword. However, when you refer to it, the underscore is at the end.
    
    The underscore after the keyword is also used for internal references, 
    citations, aliases ... 

A second solution is to write the link inline `` using the following syntax::  

    `Python <http://www.python.org/>`_

.. _Python: http://www.python.org/


Some reST markups
=================

Many of the reST commands are based on explicit markups that look like::

    .. <name>::<arguments>
        :<option>: <option values>
        
        content
        
    Example:
    .. image:: ../images/test.png
        :width: 200pt 

Here are a few examples of markup used in reST that do not require 
any arguments or options:

.. .. seealso:: :ref:`stdlib_user`, :ref:`stdlib_reference`
	This is a simple **seealso** note with a reference.

.. .. note:: 
    This is a **note**, which contains some bullets
    
     - bullet 1
     - bullet 2

.. error::
	This is an **error** example

.. warning::
	This is a **warning** directive 

You also have **attention**, **caution**, **danger**, **hint**, **important**, 
**tip**

There are many others that requires arguments that we'll discover later on.

Code and Literal blocks
=======================

Literal code blocks are introduced by ending a paragraph with the
special marker `::`. The literal block must be indented (and, like all 
paragraphs, separated from the surrounding ones by blank lines).

This is a simple example::

    import math
    print 'import done' 


Topic directive
===============

.. topic:: Your Topic Title

    Subsequent indented lines comprise
    the body of the topic, and are
    interpreted as body elements.

Sidebar directive
=================

Using this syntax::   
  
  .. sidebar:: Sidebar Title
     :subtitle: Optional Sidebar Subtitle

     Subsequent indented lines comprise
     the body of the sidebar, and are
     interpreted as body elements.
  
it is possible to create a sidebar (right)
  
.. sidebar:: Sidebar Title
   :subtitle: Optional Sidebar Subtitle

   Subsequent indented lines comprise
   the body of the sidebar, and are
   interpreted as body elements.
   
Footnote
========
   
For footnotes, use ``[#name]_`` to mark the footnote location, and add the 
footnote body at the bottom of the document after a “Footnotes” rubric 
heading, like so::

  Lorem ipsum [#f1]_ dolor sit amet ... [#f2]_

  .. rubric:: Footnotes

  .. [#f1] Text of the first footnote.
  .. [#f2] Text of the second footnote.

You can also explicitly number the footnotes (``[1]_``) or use auto-numbered 
footnotes without names (``[#]_``). Here is an example [#footnote1]_.

Citations
=========

Citation references, like [CIT2002]_ may be defined at the bottom of the page::

    .. [CIT2002] A citation
       (as often used in journals).

aliases and substitutions
=========================

If you have long text to include several times, you can create aliases::

    .. |logo| image:: ../images/wiki_logo_openalea.png
        :width: 20pt
        :height: 20pt
        
    .. |longtext| replace:: this is a long text    
        
And then call `|logo|`, which in this example inserts an image in the text |logo|.
This is especialling useful when dealing with complicated code. For instance, 
include 2 images within a table becomes easy::

    +---------+------------+
    | |logo|  | |logo|     |
    +---------+------------+
    
+---------+---------+-----------+
| |logo|  | |logo|  | |longtext||
+---------+---------+-----------+
        
        
Field list
==========

:Whatever: this is handy to create new field 

::
    :Whatever: this is handy to create new field
        

internal hyperlink
==================

Creating hyperlink is easy and is done by creating a hyperlink as follows::

    .. _begin:

And then inserting ``begin_`` in your text. For instance, jump to the beginning 
rst_tutorial_  

Titles are targets, too and implict references, like `Field list`_. are possible
 
 
python doctest
==============

you may want to include test directly within your docstring adding::
 
    >>> import math
    >>> print math.sqrt(2.)
     
and making your module executable with::

    if __name__=="__main__":
        import doctest
        doctest.testmod()
        
Then, run ``python <name.py>``
        
See ` <http://docs.python.org/library/doctest.html>`_ for a complete description


 
---------  

.. -------------------------------------------------------------------------
.. Here below are coded the different aliases, reference, citation
.. There do not appear like so in the text but can be use for references

.. |logo| image:: ../images/wiki_logo_openalea.png  
    :width: 30pt
    :height: 30pt
    :align: middle

.. |longtext| replace:: this is a longish text to include within a table and 
    which is longer than the width of the column.

     
.. rubric:: Footnotes

.. [#footnote1] this is a footnote aimed at illustrating the footnote capability.
  
.. [CIT2002] A citation
   (as often used in journals).
