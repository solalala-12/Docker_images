from flask import Flask, jsonify
import time
from tasks import make_celery

flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL='amqp://rabbit_sora:dlthfk77@localhost/rabbit',
    CELERY_RESULT_BACKEND='rpc://'
)
celery = make_celery(flask_app)


@flask_app.route("/")
def print_result():
    result = add_together.delay(23, 42)
    result.wait()  # 65
    print("yes")
    return result

@celery.task()
def add_together(a, b):
    return a + b

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0',debug=True)