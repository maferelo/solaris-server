release: python manage.py migrate

web: daphne config.asgi:application
worker: REMAP_SIGTERM=SIGQUIT celery -A config.celery_app worker --loglevel=info
beat: REMAP_SIGTERM=SIGQUIT celery -A config.celery_app beat --loglevel=info
