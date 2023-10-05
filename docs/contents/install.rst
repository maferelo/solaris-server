Install
======================================================================

Prerequisites
----------------------------------------------------------------------

* Docker; if you don't have it yet, follow the `installation instructions`_

.. _`installation instructions`: https://docs.docker.com/install/#supported-platforms

Build the Stack
---------------

This can take a while, especially the first time you run this particular command on your development system::

    $ docker compose -f local.yml build

Generally, if you want to emulate production environment use ``production.yml`` instead. And this is true for any other actions you might need to perform: whenever a switch is required, just do it!

Run the Stack
-------------

This brings up both Django and PostgreSQL. The first time it is run it might take a while to get started, but subsequent runs will occur quickly.

Open a terminal at the project root and run the following for local development::

    $ docker compose -f local.yml up

To run in a detached (background) mode, just::

    $ docker compose -f local.yml up -d

The site should start and be accessible at http://localhost:8000.

Execute Management Commands
---------------------------

As with any shell command that we wish to run in our container, this is done using the ``docker compose -f local.yml run --rm`` command: ::

    $ docker compose -f local.yml run --rm django python manage.py migrate
    $ docker compose -f local.yml run --rm django python manage.py createsuperuser

Here, ``django`` is the target service we are executing the commands against.
Also, please note that the ``docker exec`` does not work for running management commands.
