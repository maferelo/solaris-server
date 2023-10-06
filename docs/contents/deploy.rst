Deploy
======================================================================

Deploy to Heroku
----------------------------------------------------------------------



Create Heroku app::

    heroku create <app-name>

Enable container registry::

    heroku container:login

Enable container registry::

    docker build -t registry.heroku.com/<app-name>/<process-type> .

Make sure to replace `<process-type>` with `web` since this will be for a `web process <https://devcenter.heroku.com/articles/procfile#the-web-process-type>`_.

Push the image to the registry::

    docker push registry.heroku.com/<app-name>/<process-type>

Release the image to your app::

    heroku container:release <process-type> --app <app-name>

Check the logs::

    heroku logs --tail

Open the app in your browser::

    heroku open