/etc/init.d/rabbitmq-server start -detached

rabbitmq-plugins enable rabbitmq_management

rabbitmqctl add_user rabbit_sora dlthfk77
rabbitmqctl add_vhost rabbit
rabbitmqctl set_permissions -p rabbit rabbit_sora ".*" ".*" ".*"



celery -A app.celery worker --loglevel=INFO -f logs/celery_info.log --concurrency=2  &

gunicorn -w6 app:app -b 0.0.0.0:5000 --access-logfile logs/gunicorn_access.log --error-logfile logs/gunicorn_error.log &