from os import environ

bind = '0.0.0.0:' + environ.get('APP_PORT', '8080')
worker_class = 'uvicorn.workers.UvicornWorker'
max_requests = 1000
workers = int(environ.get('APP_WORKERS', 1))