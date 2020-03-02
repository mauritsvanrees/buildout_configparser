# -*- coding: utf-8 -*-
from buildout_configparser import configparser

try:
    # Python 3
    import io as StringIO
except ImportError:
    # Python 2
    import StringIO


def parse(config, *args, **kw):
    return configparser.parse(StringIO.StringIO(config), "test", *args, **kw)


def test_well_formed():
    # First, an example that illustrates a well-formed configuration.
    text = """
[s1]
a = 1

[   s2  ]         # a comment
long = a
    b

    c
l2 =


    a


    # not a comment

# comment
; also a coment

    b

      c


empty =

c=1

b    += 1

[s3]; comment
x =           a b
"""
    assert parse(text) == {
        "s1": {"a": "1"},
        "s2": {
            "b    +": "1",
            "c": "1",
            "empty": "",
            "l2": "a\n\n\n# not a comment\n\n\nb\n\n  c",
            "long": "a\nb\nc",
        },
        "s3": {"x": "a b"},
    }


def test_leading_blank_lines():
    # Here is an example with leading blank lines:

    text = "\n\n[buildout]\nz=1\n\n"
    assert parse(text) == {"buildout": {"z": "1"}}


def test_blank_non_comment_line():
    # From email:
    # "It fails when the first non-comment line after a section (even an
    # otherwise empty section) is blank.  For example:"

    text = """
[buildout]

parts = hello
versions = versions

[versions]
# Add any version pins here.

[hello]

recipe = collective.recipe.cmd
on_install = true

on_update = true
cmds = echo Hello
"""

    assert parse(text) == {
        "buildout": {"parts": "hello", "versions": "versions"},
        "hello": {
            "cmds": "echo Hello",
            "on_install": "true",
            "on_update": "true",
            "recipe": "collective.recipe.cmd",
        },
        "versions": {},
    }


def test_header_expressions():
    # Sections headers can contain an optional arbitrary Python expression.
    # When the expression evaluates to false the whole section is skipped.
    # Several sections can have the same name with different expressions, enabling
    # conditional exclusion of sections.
    text = """
[s1: 2 + 2 == 4] # this expression is true [therefore "this section" _will_ be NOT skipped
a = 1

[   s2 : 2 + 2 == 5  ]         # comment: this expression is false, so this section will be ignored]
long = a

[   s2 : 41 + 1 == 42  ]  # a comment: this expression is [true], so this section will be kept
long = b

[s3:2 in map(lambda i:i*2, [i for i in range(10)])] ;# Complex expressions are [possible!];, though they should not be (abused:)
# this section will not be skipped
long = c
"""

    assert parse(text) == {"s1": {"a": "1"}, "s2": {"long": "b"}, "s3": {"long": "c"}}


def test_title_line_trailing_comments():
    # Title line optional trailing comments are separated by a hash '#' or semicolon
    # ';' character.  The expression is an arbitrary expression with one restriction:
    # it cannot contain a literal hash '#' or semicolon ';' character: these need to be
    # string-escaped.
    # The comment can contain arbitrary characters, including brackets that are also
    # used to mark the end of a section header and may be ambiguous to recognize in
    # some cases. For example, valid sections lines include::
    text = """
[ a ]
a=1

[ b ]  # []
b=1

[ c : True ]  # ]
c =1

[ d :  True]  # []
d=1

[ e ]  # []
e = 1

[ f ]  # ]
f = 1

[g:2 in map(lambda i:i*2, ['''\x23\x3b)'''] + [i for i in range(10)] + list('\x23[]][\x3b\x23'))] # Complex #expressions; ][are [possible!] and can us escaped # and ; in literals
g = 1

[ h : True ]  ; ]
h =1

[ i :  True]  ; []
i=1

[j:2 in map(lambda i:i*2, ['''\x23\x3b)'''] + [i for i in range(10)] + list('\x23[]][\x3b\x23'))] ; Complex #expressions; ][are [possible!] and can us escaped # and ; in literals
j = 1
"""

    assert parse(text) == {
        "a": {"a": "1"},
        "b": {"b": "1"},
        "c": {"c": "1"},
        "d": {"d": "1"},
        "e": {"e": "1"},
        "f": {"f": "1"},
        "g": {"g": "1"},
        "h": {"h": "1"},
        "i": {"i": "1"},
        "j": {"j": "1"},
    }
