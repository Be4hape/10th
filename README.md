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


파이썬 데이터 타입
1. Numeric type
	1. int
	2. float
	3. complex(복소)
2. Dictionary
3. Sequence Type
	1. list
	2. tuple
	3. strings
4. Set


파이썬 나누기 연산자 : /, //, %
/ : 몫이 소수점 형태로 나옴.
// : 몫이 정수 형태로
% : 나머지


문자열 연산 : 
full_greeting = greeting + "My name is" + name
print(full_greeting)

>> hello, world my name is alice

*print 작동
name = input("input name : ")
print("hello", name, "sir!")
> hello 'name' sir!


1. *list
> l = [1,2,3,4,5]
l1 = l[0]
l5 = l[-1]
l1_l2 = l[0:2] # 슬라이싱 숫자부터 N - 1, 1과 2를 가져온다.

리스트에서 자주 사용하는 함수들
- append(x)     맨 뒤에 추가
- insert(i,x)   지정 위치에 추가
- remove(x)     해당 요소 삭제, 해당 값이 여러개라면 앞의 인덱스인 숫자만 지우고 함수 종료
- pop()         마지막 요소 꺼내기, 꺼낸다는 의미는 반환값이 있다는 것
- sort()        오름차순 정렬

ex.
3명의 나이가 적힌 종이 [20, 10, 30]
나이가 많은 순서대로 10씩 더해서 출력해라
> 순서를 정렬하고(sort), pop으로 뒤에서부터 꺼내서 10을 더함



2. 튜플
s = (10, 20)
() 순서가 있음, 값을 변경할 수 없다.
다만, [(30, 40), (10, 20)] 같은 식으로 튜플끼리의 그룹화가 되어있으면 이 그룹끼리는 정렬이나 위치 변환이 가능
속도가 list, 딕셔너리보다 빠름
좌표값에 주로 사용



3.*딕셔너리
# key(키), value(값)
# { }
student = {
    "name"  : "asd",
    "age"   : 25,
    "mahor" : "DA"
}
b = student["name"]
print(b) #asd
> 값에 접근하기 위해 key를 사용함

# key 값 다 가져오기
student.keys()
# value 값 다 가져오기
student.values()
# 키, 값 모두 가져오기
student.items()

**없는 값에 접근할 때
script 특성 상 에러가 발생하면 코드가 멈추기 때문에, 
에러가 발생하더라도 NONE만 출력하고 코드를 모두 실행하고 싶다면 get()으로 접근한다.**



## *리스트 안에 딕셔너리
students = [
    {"name": "Hannah", "age": 25, "score": 90},
    {"name": "Minji", "age": 21, "score": 85},
    {"name": "Yumi", "age": 23, "score": 95}
]
> 리스트로 인덱스 부여, 딕셔너리로 키와 밸류를 준다





## 25.11.11. Pythonic한 함수 - enumerate()
ex. 3개의 글자를 담고 있는 리스트를 대상으로 루프를 돌면서 글자를 출력하는 코드

for letter in ['A', 'B', 'C']:
    print(letter)


여기에 인덱스도 같이 출력하고 싶다면,
i = 0
for letter in ['A', 'B', 'C']:
    print(i, letter)
    i += 1
다른 언어를 사용했던 사람이라면 흔히 이런식으로 사용하지만
i가 for문이 종료된 이후에도 네임스페이스에 남아있기 때문에 이상적이지는 않다.

혹은
letters = ['A', 'B', 'C']
for i in range(len(letters)):
    letter = letters[i]
    print(i, letter)
이런식으로도 할 수 있지만, 이는 Pythonic하지 않아 보인다고 한다.


내장함수인 enumerate() 사용, 인덱스와 원소를 동시에 접근하면서 루프를 돌릴 수 있다.
for entry in enumerate(['A', 'B', 'C']):
    print(entry)


















