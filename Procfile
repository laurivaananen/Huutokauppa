web: gunicorn application:app --preload
worker: celery -A application.celery worker
