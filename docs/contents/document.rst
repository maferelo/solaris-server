Document
======================================================================

Get Started
----------------------------------------------------------------------

Documentation can be written as rst files in `docs/contents/`.


To build and serve docs, use the commands::

    docker compose -f local.yml up docs



Navigate to port 9000 on your host to see the documentation. This will be opened automatically at `localhost <http://localhost:9000/>`_.

`Sphinx <https://www.sphinx-doc.org/>`_ is the tool used to build documentation.

Docstrings to Documentation
----------------------------------------------------------------------

The sphinx extension `apidoc <https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html/>`_ is used to automatically document code using signatures and docstrings.

Docstrings will be picked up from project files and available for documentation. See the `Napoleon <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/>`_ extension for details.

To compile all docstrings automatically into documentation source files, use the command:
    ::

        docker run --rm docs make apidocs
