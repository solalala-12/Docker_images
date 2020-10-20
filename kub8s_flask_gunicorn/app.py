import os
from flask import Flask, url_for, jsonify, request, make_response,render_template
from celery import Celery, states
import time
import pysftp
# from flask_cors import CORS, cross_origin

app = Flask(__name__)
# 보안 모델
# CORS(app)

app.config['CELERY_BROKER_URL'] = 'amqp://rabbit_sora:dlthfk77@localhost/rabbit'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@app.route('/',methods=['GET'])
def index():
    x = request.args.get("model")
    if x=='ex':
        get_model()
        return 'Done'
    return 'Failed'
        

@celery.task(bind=True)
def get_model(self):

    myHostname = "169.56.76.27"
    myUsername = "analy"
    myPassword = "Kyowon2017!"

    with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
        print ("Connection succesfully stablished ... ")
    # Define the file that you want to download from the remote directory
        remoteFilePath = '/data01/logs/analy/maipksap01.allng.com/batch/ir_get_item_parameters_drl.log'
        localFilePath = './test.log'

        sftp.get(remoteFilePath, localFilePath)
    




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

# docker exec -it flask_sora /bin/bash -c "sh start_celery.sh"
# /data01/logs/analy/maipksap01.allng.com/batch/ir_get_item_parameters_drl.log