=====
Usage
=====

To use Run Inside in a project::

    import runinside

From the command line, try something like::

    runinside -s "*.py" -m manifestfile.txt -c mycontainer "ls | grep py"

Commandline switches
--------------------

.. code-block::

    Usage: runinside [OPTIONS] [EXECUTION]

    Options:
    -s, --source PATH       Source file.  For multiples, use wildcards or a
                            manifest.

    -m, --manifest PATH     Manifest of files to copy into the container.
    -d, --destination PATH  Destination directory inside the container.
    -c, --container TEXT    Target container by name or ID.  [required]
    --help                  Show this message and exit.
..



