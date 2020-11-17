import os

from flask import Flask, url_for, jsonify, request, make_response,render_template
from celery import Celery, states
import time
# from flask_cors import CORS, cross_origin

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import pysftp
import logging
import zipfile
import sys

import json
import numpy as np




# 환경변수 , 
model_type=os.environ['MODEL_TYPE']
model_name=os.environ['MODEL_NAME']
tf_sess=None
today=None
target_model=None

# 변경가능

sys.path.append('./'+model_name+'/src/')

sys.path.append('./'+model_name+'/model/')

# 로그 생성
logger = logging.getLogger()
# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# log를 파일에 출력
file_handler = logging.FileHandler('./logs/my.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



app = Flask(__name__)
# 보안 모델
# CORS(app)

app.config['CELERY_BROKER_URL'] = 'amqp://rabbit_sora:dlthfk77@localhost/rabbit'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'
app.config['JSON_AS_ASCII']=False

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)





@app.route('/post',methods=['POST']) 
def hi():

    global target_model

    data = request.get_json(force=True)

    input_data = data["test"]

    if model_type=='sklearn':
        print('모델 정보 :', target_model)

        result = target_model.predict(input_data)
    else:
        global tf_sess

        print('세션 정보 : ',tf_sess)
        os.chdir("/root/model_rest_api/"+model_name+'/src/')
        result = target_model.predict(tf_sess,input_data)


    if type(result).__module__ == np.__name__:


        result_dict={'result':result.tolist()}
    else:
        result_dict={'result':result}


    resp = make_response(jsonify(result_dict))

    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
    
    



@app.route('/model_download')
def model_download():

    
    
    check_model_state=download(target='model')
    _ = model_load()

    if not check_model_state:
        return '* * * * Failed download model * * * *'
    else:
        return '* * * * Succeeded download model * * * * \n'+ str(target_model) 



@app.route('/src_download')
def src_download():
    
    check_model_state=download(target='src')
    # os.system('pip3 install -r {}'.format(model_name+'/src/'+'requirements.txt'))

    if not check_model_state:
        return '* * * * Failed download src * * * * ' 
    else:
        return '* * * * Succeeded download src * * * * \n'+ str(check_model_state) 
     
def download(target):
    x=True
    # model_path='./'+ os.environ['MODEL_NAME']
    
    x = download_from_azure(target)
    # sftp
    if not x:
        logger.info(" * * * Downloaded from sftp * * *")
        x= download_from_sftp(target)
    else:
        logger.info(" * * * Downloaded from Azure * * * ")
    
    return x

        #logger.info(" * * * Already model file exists * * * ")
    
    

def download_from_azure(target):


    name_list=[]

    # model_name=os.getenv('MODEL_NAME')

    try:
        connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        container_name = "edu"
        container_client = blob_service_client.get_container_client(container_name)
        
        # path in azure

        pwd=os.getcwd()
        if target=='src':
            blob_path = "/ysh_databricks/"+model_name+'/src/'
            local_path_parent_folder=os.path.join(pwd,model_name,'src')
        else:
            blob_path = "/ysh_databricks/"+model_name+'/model/'
            local_path_parent_folder=os.path.join(pwd,model_name,'model')

        if not os.path.exists(local_path_parent_folder):
            os.makedirs(local_path_parent_folder)


        blob_list  = container_client.list_blobs(blob_path)
       

        if target=='src':
            blob_path = blob_path+model_name+'.zip'
            local_path_file= os.path.join(model_name,'src',model_name)+'.zip'  

            logger.info(blob_path)
            logger.info(local_path_file)

        else:

            for blob in blob_list:
                print(blob)

                _, tail = os.path.split("{}".format(blob.name))
                name_list.append(int(tail[:8]))
            
            today=str(sorted(name_list)[-1])

            
            blob_path =blob_path+today+'.zip'
            local_path_file= os.path.join(model_name,'model',today)+'.zip'  


        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_path)



        with open(local_path_file, "wb") as my_blob:
            download_stream = blob_client.download_blob()
            my_blob.write(download_stream.readall())
        
        
        with zipfile.ZipFile(local_path_file, 'r') as zip_ref:
            zip_ref.extractall(local_path_parent_folder)
                
        
    except Exception as ex:
        print(ex)
        logger.info(ex)

        return False

    print("에져 다운로드 성공")
    
    return True




def download_from_sftp(target):

    
    myHostname = os.environ['MY_HOST_NAME']
    myUsername = os.environ['MY_USER_NAME']
    myPassword = os.environ['MY_PASSWORD']

    
    '''
    myHostname = "169.56.76.27"
    myUsername = "d0106"
    myPassword = "d0106!@#$"
    '''
    try: 
        with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:

            print ("Connection succesfully stablished ... ")

            if target=='src':
                remoteFilePath = '/home/d0106/'+model_name+'/src/'+model_name+'.zip'
                localFilePath = './'+model_name+'/src/'+model_name+'.zip'
            else:
                remoteFilePath = '/home/d0106/'+model_name+'/model/'
                name_list = sftp.listdir(remoteFilePath)
                
                today=sorted([int(i[0:8]) for i in name_list])[-1]
                
                remoteFilePath= '/home/d0106/'+model_name+'/model/'+str(today)+'.zip'
                localFilePath = './'+model_name+'/model/'+str(today)+'.zip'



            sftp.get(remoteFilePath, localFilePath)
            print(remoteFilePath,localFilePath)
            #sftp.get_d(remoteFilePath, localFilePath, preserve_mtime=True)


            if target=='src':
                target_dir='./'+model_name+'/src/'
            else:
                target_dir='./'+model_name+'/model/'

            with zipfile.ZipFile(localFilePath, 'r') as zip_ref:
                zip_ref.extractall(target_dir)


            
    except Exception as ex:
        print('-----------------------',ex)
        logger.info(ex)
        return False

    return True




@app.route('/model_load',methods=['POST'])
def model_load():
    '''
    model_type=os.getenv('MODEL_TYPE')
    model_name=os.getenv('MODEL_NAME')
    '''
    global tf_sess
    global target_model
    os.system('pip3 install -r {}'.format(model_name+'/src/'+'requirements.txt'))
    print("intall library done")
    
    try:
        target_model=None

        # scikit learn
        if model_type =='sklearn':
            import sklearn
            import joblib
            
            model_file=os.listdir(os.path.join(model_name,'model'))
            model_file=[i for i in model_file if i.endswith('.pkl')][0]
            target_model= joblib.load('./'+model_name+'/model/'+model_file)
        # tf model
        else:
            from k8s_api_model import k8s_api_model
            import tensorflow as tf
            tf.reset_default_graph()
            target_model = k8s_api_model()
            if 'build' in methods(k8s_api_model):
                target_model.build()
            # if build -> build / x -> x
            try:
                tf_sess = target_model.load('./'+model_name+'/model')
            except Exception as ex:
                logger.info(ex)
    
    except Exception as ex:
        logger.info(ex)
        return False

    logger.info(' * * * * Succeed load model * * * *')    
    return 'done'




            
def methods(cls):
    from types import FunctionType
    return [x for x, y in cls.__dict__.items() if type(y) == FunctionType]


if __name__ == '__main__':


    app.run(host='0.0.0.0', debug=True)


