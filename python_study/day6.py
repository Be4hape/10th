# comprehension : 반복문을 한줄로 표현하는 문법
# pythonic하게 작성하는 방법임 (깔끔, 읽기 쉬운, 일단 시도하고 처리)
# 컴프리헨션은 쓰는 사람들이 많기 때문에 알아보기 위해서라도 쓰는 방법을 알아야함

# 1. List Comprehension
## 두 케이스의 결과는 같음, 아래의 컴프리헨션은 속도도 더 빠름
# List Comprehension : [표현식 for 변수 in 반복대상 if 조건]
# 리스트 컴프리헨션은 리스트를 생성하고 for문을 사용하기 위해 사용한다.
# 따라서 표현식은 append가 가장 적합함. 다른 함수도 사용 가능함

# case1
result = []
for i in range(1, 5):
    result.append(i)
print(result)

# case2 
print([i for i in range(1, 5)])



# 표현식은 append안에 들어가는 값을 의미
# case11
result2 = []
for i in range(1, 5):
    result2.append(i**2)
print(result2)

# case22
print([i**2 for i in range(1, 6)])


# 조건문 추가
print([i**2 for i in range(1, 6) if i % 2 == 0])






# 2.Dictionary Comprehension
# { 키 표현식 : 값 표현식 for 변수 in 반복대상 if 조건 }
students = ['철수', '영희', '유선']
{ student : 0 for student in students }
# >> {'철수' : 0. '영희' : 0, '유선' : 0 }



# 초기 형태, enumerate로 i와 name을 동시에 names의 인덱스만큼 반복시킨다. 
# i번째에 name을 넣어서 list 갱신
# dic[i]:0, name:"ha"
# dic[i]:1, name:"yh"
# dic[i]:2, name:jh
names = ["ha", "yh", "jh"]
dic = {}
for i, name in enumerate(names) : 
    dic[i] = name



## enumerate 는 자동으로 인덱스, 값으로 생성한다.
# 실행 결과는 (0 : "ha"), (1 : "yh"), (2 : "jh") 같은 식으로 자동으로 배치됨, 튜플 형태
names = ["ha", "yh", "jh"]
re = {i : name for i, name in enumerate(names)}










# 컴프리센션, 예외 처리 -> 파이썬이라서 더 중요한 문법
# 파이써닉(pythonic) 깔끔하고 읽기 좋은 코드로 작성, 일단 시도하고 처리

# 컴프리헨션: 반복문을 한 줄로 줄이는 문법
# for, if
# 컴프리헨션 주의사항: 식 자체가 너무 복잡해지면 사용하면 안 됨

# 리스트 컴프리헨션
# [ 표현식 for 변수 in 반복대상 if 조건문 ]

result=[]
for i in range(1, 5):
    result.append(i)
# print(result) # [1, 2, 3, 4]
# print([i for i in range(1, 5)]) # [1, 2, 3, 4] 리스트 선언, append

result=[]
for i in range(1, 6):
    result.append(i**2)

[i**2 for i in range(1, 6)]

result=[]
for i in range(1,6):
    if(i % 2 == 0):
        result.append(i**2)

[i**2 for i in range(1, 6) if i % 2 == 0]


# 딕셔너리 컴프리헨션 -> 키, 값
# { 키표현식: 값표현식 for 변수 in 반복대상 if 조건 }
students = ['철수', '영희', '유선']
{ student: 0 for student in students }
# {'철수': 0, '영희': 0, '유선': 0}

words = ["Python", "Data", "AI"]
lengths = {word: len(word) for word in words}

result = {w: len(w) for w in words if len(w) >= 3}


nums = [1, 2, 3, 4, 5] # 1: 1^2, 2: 2^2
sq = {n: n**2 for n in nums}

# 키 값 -> for 생성 숫자값으로
# [1, 2, 3] 0: 1, 1: 2, 2: 3
names = ["ha", "yh", "jh"]
re = {i: name for i, name in enumerate(names)}

# enumerate -> 자동으로 인덱스, 값 -> 쌍으로 생성
names = ["ha", "yh", "jh"]
dict = {}
for i, name in enumerate(names): # (0, "ha"), (1, "yh"), (2, "jh")
    dict[i] = name;
