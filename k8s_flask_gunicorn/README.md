#  모델 소스 관리

Rest API에 필요한 모듈과 코드는 **zip형태로** Storage(Cloud or NAS or Server)에서 관리함.  
모델과 소스는 파일명이 같을 때 자동 덮어쓰기 함.
모델은 YYYYMMDD.zip 으로 관리하며 소스는 model_name.zip으로 관리한다.
 

> ex)
> model_name= test_model로 설정 시,
 model path = ./test_model/model/20201104.zip  
 sources path = ./test_model/src/test_model.zip



#  1. 환경 세팅

 1. Install Docker
 2. Install K8s
 3. Docker image build 
 4. pod-info.yaml 환경변수 세팅 (hostPath, MODEL_NAME, MODEL_TYPE, 인증 정보 등)
 5. K8s 컨테이너 실행
	 `kubectl apply -f pod-info.yaml`
	 
6. `python3 app.py`
 

# 2. 모델 & 모듈 소스 다운로드

 컨테이너 최초 실행 시 모델, 모듈 소스가 로컬에 존재 해야하고 컨테이너가 실행 될 때 이전 모델 로드가 되어있는 상태.

 - Source Download  [http://{serverIp}:{serverPort}/src_download](http://%7bserverIp%7d:%7bserverPort%7d/src_download)  
- Model  Download [http://{serverIp}:{serverPort}/model_download](http://%7bserverIp%7d:%7bserverPort%7d/model_download)  
  


> 소스 다운로드 후 로드 되어있던 모델로 Test 진행.  
모델 다운로드 후 변경 모델로 Test 진행.  


##  소스 구성 

 - Tensorflow

	ㅡ src/
	|ㅡㅡ requirements.txt
	|ㅡㅡ*model_sources_files*
	ㅡmodel/
	|ㅡㅡ*model_checkpoint_files*
	
```
class ex_model(object):
	def __init__(self):
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



 - Scikit-Learn
	ㅡ src/
	|ㅡㅡ requirements.txt
	|ㅡㅡmodel_sources_files
	ㅡmodel/
	|ㅡㅡmodel_checkpoint_files(.pkl)
