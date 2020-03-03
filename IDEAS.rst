Future ideas
============

The basic configparser.py from buildout was added as a first step.
Maybe this is enough, but we could include more:

- ``_default_globals`` from ``buildout.py`` for expressions.
- Import the main usable functions and classes in ``__init__.py`` or a new ``api.py``.
- Support the ``extends`` keyword (``buildout.py``) and read those files when they are local.
- Support ``-=`` and ``+=`` when using ``extends``.
- Add support for downloading external configs (various parts from ``download.py`` and ``buildout.py``).
- The ``annotate`` command from buildout, so we can see from which ``extends`` file a config option comes.

Most of those are about ``extends``.
This may be a bit much to incorporate, and we may not need it.

**Main reason** for me to try to separate the configparser from zc.buildout,
is to be able to parse the ``[versions]`` section and output a ``constraints.txt`` for ``pip``.
There is an old buildout extension ``buildout.requirements`` which can do this,
but this works by keeping track of which versions buildout installs, and I don't want buildout to install anything.

I would prefer it the other way around: let buildout read a constraints and/or requirements file.
Perhaps that could be done in a buildout extension.
But you need a way to take a current buildout config with traditional version pins and make a constraints file of it.

The mapping would be:

- ``constraints.txt`` maps to ``[versions]``
- ``requirements.txt`` maps to ``[buildout] eggs=``

And with development checkouts (``-e git+git@...``):

- ``constraints.txt``  maps to ``[sources]`` from ``mr.developer``.
- ``requirements.txt`` additionally maps to ``[buildout] auto-checkout=``.

Separating the configparser may be nice, but for outputting constraints and requirements we could just use the version code that is in ``zc.buildout``.
At least for the moment, ``configparser.py`` in this package is a simply copy, except that I ran the ``black`` code formatter over it.
And we could use the actual ``Buildout`` object::

    from zc.buildout.buildout import Buildout
    # next line may take a few seconds, but seems reasonable
    b = Buildout('buildout.cfg', [])
    b['versions'].items()
    b['versions']['setuptools'] == '42.0.2'

This may create a few directories (like ``eggs`` and ``downloads``), but does not actually install anything it seems.
