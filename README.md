11.03. 원유선 튜터님
프로젝트마다 라이브러리를 불러오는 버전이 충돌이 날 수 있음.
보통 프젝별로 버전을 관리하는데, 이를 가상환경 관리라고 함.

>python -m venv venv
 가상환경 세팅 명령어

새로운 폴더를 만들었다면, 그 환경에서도 가상환경 세팅을 해야함 - 프젝별로 버전을 맞추기 위해


기본적으로 vemv 파일을 만들어 그 안에서 pip list에 있는 라이브러리들을 관리하는 형태,


powershell로 작업을 진행 중 : venv\bin\activate 명령어로 venv에 activate 된 상태임
다 사용했다면 deactivate로 활성화 해제를 해야한다.


python 파일 디버깅 : python day1.py 
>> day1.py 파일을 디버깅한다.