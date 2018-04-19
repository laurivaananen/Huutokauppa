web: gunicorn application:app --preload
worker: celery worker --app=application/items/tasks.app
