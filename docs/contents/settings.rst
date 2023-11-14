Settings
========

This project relies extensively on environment settings which **will not work with Apache/mod_wsgi setups**. It has been deployed successfully with both Gunicorn/Nginx and even uWSGI/Nginx.

For configuration purposes, the following table maps environment variables to their Django setting and project settings:

======================================= =========================== ============================================== ======================================================================
Environment Variable                    Django Setting              Development Default                            Production Default
======================================= =========================== ============================================== ======================================================================
DATABASE_URL                            DATABASES                   auto w/ Docker; postgres://project_slug w/o    raises error
DJANGO_ADMIN_URL                        n/a                         'admin/'                                       raises error
DJANGO_DEBUG                            DEBUG                       True                                           False
DJANGO_SECRET_KEY                       SECRET_KEY                  auto-generated                                 raises error
DJANGO_SESSION_COOKIE_HTTPONLY          SESSION_COOKIE_HTTPONLY     n/a                                            True
DJANGO_SESSION_COOKIE_SECURE            SESSION_COOKIE_SECURE       n/a                                            False
DJANGO_ALLOWED_HOSTS                    ALLOWED_HOSTS               ['*']                                          ['your_domain_name']
======================================= =========================== ============================================== ======================================================================

The following table lists settings and their defaults for third-party applications, which may or may not be part of your project:

======================================= =========================== ============================================== ======================================================================
Environment Variable                    Django Setting              Development Default                            Production Default
======================================= =========================== ============================================== ======================================================================
======================================= =========================== ============================================== ======================================================================

--------------------------
Other Environment Settings
--------------------------

DJANGO_ACCOUNT_ALLOW_REGISTRATION (=True)
    Allow enable or disable user registration through `django-allauth` without disabling other characteristics like authentication and account management. (Django Setting: ACCOUNT_ALLOW_REGISTRATION)

DJANGO_ADMIN_FORCE_ALLAUTH (=False)
    Force the `admin` sign in process to go through the `django-allauth` workflow.
