/etc/init.d/rabbitmq-server start -detached
rabbitmq-plugins enable rabbitmq_management
rabbitmqctl add_user rabbit_sora12 dlthfk77
rabbitmqctl add_vhost rabbit1
rabbitmqctl set_permissions -p rabbit1 rabbit_sora12 ".*" ".*" ".*"
celery -A app.celery worker --loglevel=INFO -f logs/celery_info.log --concurrency=2  &

gunicorn -w6 app:app -b 0.0.0.0:5000 --access-logfile logs/gunicorn_access.log --error-logfile logs/gunicorn_error.log --preload --timeout 400

