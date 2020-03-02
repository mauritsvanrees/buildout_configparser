buildout_configparser
=====================

This is a configparser taken from Buildout.

This readme mostly describes the configuration file syntax.

Buildout configurations use an `INI file format
<https://en.wikipedia.org/wiki/INI_file>`_.

A configuration is a collection of named sections containing named
options.

Section names
-------------

A section begins with a section and, optionally, a condition in
square braces (``[`` and ``]``).

A name can consist of any characters other than whitespace, square
braces, curly braces (``{`` or ``}``), pound signs (``#``), colons
(``:``) or semi-colons (``;``).  The name may be surrounded by leading
and trailing whitespace, which is ignored.

An optional condition is separated from the name by a colon and is a
Python expression.  It may not contain a pound sign or semi-colon.  See
the section on :ref:`conditional sections <conditional-sections>` for
an example and more details.

A comment, preceded by a pound sign or semicolon may follow the
section name, as in:

.. code-block:: ini

   [buildout] # This is the buildout section

.. -> header

Options
-------

Options are specified with an option name followed by an equal sign
and a value:

.. code-block:: ini

   parts = py

.. -> option

    >>> import six
    >>> import zc.buildout.configparser
    >>> def parse(s):
    ...     return zc.buildout.configparser.parse(six.StringIO(s), 'test')
    >>> from pprint import pprint
    >>> pprint(parse(header + option))
    {'buildout': {'parts': 'py'}}

Option names may have any characters other than whitespace, square
braces, curly braces, equal signs, or colons.  There may be and
usually is whitespace between the name and the equal sign and the name
and equal sign must be on the same line.  Names starting with ``<``
are reserved for Buildout's use.

Option values may contain any characters. A consequence of this is
that there can't be comments in option values.

Option values may be continued on multiple lines, and may contain blank lines:

.. code-block:: ini

   parts = py

           test

.. -> option

Whitespace in option values
___________________________

Trailing whitespace is stripped from each line in an option value.
Leading and trailing blank lines are stripped from option values.

Handling of leading whitespace and blank lines internal to values
depend on whether there is data on the first line (containing the
option name).

data on the first line
  Leading whitespace is stripped and blank lines are omitted.

  The resulting option value in the example above is:

  .. code-block:: ini

        py
        test

  .. -> val

      >>> eq(parse(header + option)['buildout']['parts'] + '\n', val)

no data on the first line
  Internal blank lines are retained and common leading white space is stripped.

  For example, the value of the option:

  .. code-block:: ini

     code =
         if x == 1:
             y = 2 # a comment

             return

  .. -> option

  is::

     if x == 1:
         y = 2 # a comment

         return

  .. -> val

       >>> eq(parse(header + option)['buildout']['code'] + '\n', val)

Special "implication" syntax for the ``<part-dependencies>`` option
____________________________________________________________________

An exception to the normal option syntax is the use of ``=>`` as a
short-hand for the ``<part-dependencies>`` option:

.. code-block:: ini

   => part1 part2
      part3

This is equivalent to:

.. code-block:: ini

   <part-dependencies> = part1 part2
      part3

and declares that the named parts are dependencies of the part in
which this option appears.

Comments and blank lines
------------------------

Lines beginning with pound signs or semi-colons (``#`` or ``;``) are
comments::

  # This is a comment
  ; This too

.. -> comment

       >>> eq(parse(comment + header + comment + option + comment )
       ...    ['buildout']['code'] + '\n', val)

As mentioned earlier, comments can also appear after section names.

Blank lines are ignored unless they're within option values that only
have data on continuation lines.

.. [#root-logger] Generally, the root logger format is used for all
   messages unless it is overridden by a lower-level logger.

.. [#socket-timeout] This timeout reflects how long to wait on
   individual socket operations. A slow request may take much longer
   than this timeout.

