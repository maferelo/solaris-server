Deploy
======================================================================

Deploy to Heroku
----------------------------------------------------------------------

Script
------

Run these commands to deploy the project to Heroku:

.. code-block:: bash

    heroku create --buildpack heroku/python omibus-server-staging

    heroku addons:create heroku-postgresql:essential-0 --app omibus-server-staging

    heroku pg:psql DATABASE_URL -a omibus-server-staging
    # CREATE EXTENSION postgis;

    heroku addons:create heroku-redis:mini --app omibus-server-staging
    # Set the broker URL to Redis
    heroku config:set CELERY_BROKER_URL=`heroku config:get REDIS_URL` --app omibus-server-staging
    # Scale dyno to 1 instance
    heroku ps:scale worker=1 -a omibus-server-staging

    heroku config:set PYTHONHASHSEED=random -a omibus-server-staging

    heroku config:set WEB_CONCURRENCY=4 -a omibus-server-staging

    heroku config:set DJANGO_DEBUG=False -a omibus-server-staging
    heroku config:set DJANGO_SETTINGS_MODULE=config.settings.production -a omibus-server-staging
    heroku config:set DJANGO_SECRET_KEY=$(openssl rand -base64 32) -a omibus-server-staging

    # Generating a 32 character-long random string without any of the visually similar characters "IOl01":
    heroku config:set DJANGO_ADMIN_URL="$(openssl rand -base64 4096 | tr -dc 'A-HJ-NP-Za-km-z2-9' | head -c 32)/" -a omibus-server-staging

    # Set this to your Heroku app url, e.g. 'bionic-beaver-28392.herokuapp.com'
    heroku config:set DJANGO_ALLOWED_HOSTS=omibus-server-staging-c6d6ea99f779.herokuapp.com -a omibus-server-staging

    # Assign with AWS_ACCESS_KEY_ID
    heroku config:set DJANGO_AWS_ACCESS_KEY_ID= -a omibus-server-staging

    # Assign with AWS_SECRET_ACCESS_KEY
    heroku config:set DJANGO_AWS_SECRET_ACCESS_KEY= -a omibus-server-staging

    # Assign with AWS_STORAGE_BUCKET_NAME
    heroku config:set DJANGO_AWS_STORAGE_BUCKET_NAME= -a omibus-server-staging

    git push heroku dev --app omibus-server-staging

    heroku run python manage.py createsuperuser --app omibus-server-staging

    heroku run python manage.py check --deploy --app omibus-server-staging

    heroku logs --tail --app omibus-server-staging

    heroku open --app omibus-server-staging
