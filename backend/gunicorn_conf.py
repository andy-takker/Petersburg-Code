from os import environ
import logging
logger = logging.getLogger('gunicorn')
bind = '0.0.0.0:' + environ.get('APP_PORT', '8080')
logger.warning(environ.items())
worker_class = 'uvicorn.workers.UvicornWorker'
max_requests = 1000
workers = int(environ.get('APP_WORKERS', 1))
