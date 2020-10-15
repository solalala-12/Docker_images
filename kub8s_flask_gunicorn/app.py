import os
from flask import Flask, url_for, jsonify, request, make_response,render_template
from celery import Celery, states
import time
# from flask_cors import CORS, cross_origin

app = Flask(__name__)
# 보안 모델
# CORS(app)

app.config['CELERY_BROKER_URL'] = 'amqp://rabbit_sora:dlthfk77@localhost/rabbit'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@app.route('/')
def index():
    dicts=print_ex()
    return dicts

@celery.task(bind=True)
def print_ex(self):
    dicts={"result":"result"}
    return dicts



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

# docker exec -it flask_sora /bin/bash -c "sh start_celery.sh"