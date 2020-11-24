#  모델 소스 관리



- Rest API에 필요한 모듈과 코드는 **zip형태로** Storage(Cloud or NAS or Server)에서 관리함.  
- 모델과 소스는 파일명이 같을 때 자동 덮어쓰기 함.
- 모델은 YYYYMMDD.zip 형태로 관리하며 model_download url 호출 시 **가장 최근 날짜의 zip 모델**파일을 다운로드하고 자동 로드함.
-  소스는 MODEL_NAME.zip으로 관리한다.

	> ex)
	> model_name= test_model로 설정 시,
	model path = ./test_model/model/20201104.zip  
	sources path = ./test_model/src/test_model.zip



#  1. 환경 세팅

 1. Install Docker
 2. Install K8s <br>
	설치 방법 참조 (But, Docker 버전마다 UI가 다를 수 있음) <br>
	https://nirsa.tistory.com/119

 3. pod-info.yaml 환경변수 세팅 <br>
 	- hostPath : pod-info.yml이 있는 경로 (컨테이너와 로컬 공유 경로) 
	- MODEL_NAME : 모델 파일의 압축폴더 이름 
	- MODEL_TYPE : tf or sklearn
	- 클라우드 접근권한  FTP 서버 정보 등 
	 
 4. K8s 컨테이너 실행 <br>
	 `kubectl apply -f pod-info.yaml`

 5. `http://{serverIp}:{serverPort}/` <br>
	ex) `http://localhost:8000/` <br>
 	post 요청 실행(모델이 정상 로드되었는지 확인하기 위함) <br>
	모델이 정상 로드 완료 되면 {"state": "done"} 이 return된다.

 6. `http://{serverIp}:{serverPort}/result` <br>
 ex) `http://localhost:8000/result` <br>
	input : {"test": input_data} <br>
	output : {"result" : output_data}
 

# 2. 모델 & 모듈 소스 다운로드

-  컨테이너 최초 실행 시 모델, 모듈 소스가 로컬에 존재해야함. <br>
	 컨테이너가 실행 될 때 이전 모델 로드가 되어있는 상태.
- 로컬에 소스와 모델이 없거나 새로운 버전을 다운로드 할 경우 , Sources Download -> Model Download 순을 지켜야함.

	 Source Download  [http://{serverIp}:{serverPort}/src_download](http://%7bserverIp%7d:%7bserverPort%7d/src_download)  
 Model  Download [http://{serverIp}:{serverPort}/model_download](http://%7bserverIp%7d:%7bserverPort%7d/model_download)  
  


	> 소스 다운로드 후 로드 되어있던 모델로 Test 진행.  
	모델 다운로드 후 변경 모델로 Test 진행.  


# 3. 소스 구성 

### Tensorflow
- ####  workspace
	```
	│  
	└─k8s_flask
		│  app.py
		│  docker-compose.yml
		│  Dockerfile
		│  pod-info.yaml
		│  README.md
		│  requirements.txt
		│  start_celery.sh
		│  test_model.txt
		│  
		├─logs
		│      celery_info.log
		│      gunicorn_access.log
		│      gunicorn_error.log
		│      my.log
		│      
		└─test_model
			├─model
			│      20201107.zip
			│      checkpoint
			│      my_test_model-208000.data-00000-of-00001
			│      my_test_model-208000.index
			│      my_test_model-208000.meta
			│      
			└─src
				│  hangle.py
				│  k8s_api_model.py
				│  k8s_api_utils.py
				│  requirements.txt
				│  
				└─data
					  ix_to_word_3000.pkl
					  naver_news_2999_even.csv
					  word_to_ix_3000.pkl   
	```

 - #### Rules
	
	 1. model hyperparameter hard coding
	 2. load method는  항상 tf **session**을 return해야한다.
	 

	```
	@src/k8s_api_model.py

	class k8s_api_model(object):

		def __init__(self):
		
			self.source_vocab_size = 3000 # hyperparameter hard coding
				...
				
		def build(self): # 선택
				...
				
		def load(self,model_path):

			ckpt=tf.train.get_checkpoint_state(model_path)
			...
			sess = tf.Session()
			return sess
			
		def predict(self, session)
			return result
	```



 ### Scikit-Learn
- ####  workspace
	```
	│  
	└─k8s_flask
		│  app.py
		│  docker-compose.yml
		│  Dockerfile
		│  pod-info.yaml
		│  README.md
		│  requirements.txt
		│  start_celery.sh
		│  test_model.txt
		│  
		├─logs
		│      celery_info.log
		│      gunicorn_access.log
		│      gunicorn_error.log
		│      my.log
		│      
		└─test_model_sci
			├─model
			│      20201103.zip
			│      test_model_sci.pkl
			│      
			└─src
				  requirements.txt
				  test_model_sci.zip
	```