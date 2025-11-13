# csv 파일 불러오기, 노션의 school_scores.scv를 가져온다
import csv

# school csv파일을, read형식으로, 인코딩은 한국어로 가져온다.
with open("school_scores.csv", "r", encoding = "utf-8") as f :
    reader = csv.DictReader(f)
    students = list(reader)
# print(students)
'''
[{'name': 'Hannah', 'kor': '90', 'eng': '95', 'math': '85'}, 
{'name': 'Minjun', 'kor': '80', 'eng': '88', 'math': '92'}, 
{'name': 'Yujin', 'kor': '75', 'eng': '85', 'math': '100'}, 
{'name': 'Dohyeok', 'kor': '100', 'eng': '70', 'math': '88'}, 
{'name': 'Suyun', 'kor': '88', 'eng': '90', 'math': '93'}, 
{'name': 'Jiwon', 'kor': '95', 'eng': '97', 'math': '99'}, 
{'name': 'Hojun', 'kor': '65', 'eng': '75', 'math': '60'}, 
{'name': 'Yuna', 'kor': '78', 'eng': '82', 'math': '85'}, 
'name': 'Taeyang', 'kor': '92', 'eng': '89', 'math': '91'}, 
{'name': 'Seojin', 'kor': '55', 'eng': '70', 'math': '68'}]
'''
# 데이터를 먼저 확인 > 어떤 처리를 해줄 것인가?
# 점수는 지금 문자 형태로 저장되어 있음






### 데이터 전처리.


# 1. 리스트 안에 하나의 원소에 접근하자. students[i]
# 2. 딕셔너리에서는 000["key"]

for i in students : 
    # 첫번째 순회 : 리스트의 첫번째 줄
    # 두번째 순회 : 리스트의 두번째 줄
    # i["kor"] > 첫번째 줄에 kor 값을 가져온다. 즉 90을 의미.
    # int로 바꿔주기 위해 i["kor"] = int(i["kor"])
    i["kor"] = int(i["kor"]);
    i["eng"] = int(i["eng"]);
    i["math"] = int(i["math"]);

# print(students)
'''
[{'name': 'Hannah', 'kor': 90, 'eng': 95, 'math': 85}, 
{'name': 'Minjun', 'kor': 80, 'eng': 88, 'math': 92}, 
{'name': 'Yujin', 'kor': 75, 'eng': 85, 'math': 100}, 
{'name': 'Dohyeok', 'kor': 100, 'eng': 70, 'math': 88}, 
{'name': 'Suyun', 'kor': 88, 'eng': 90, 'math': 93}, 
{'name': 'Jiwon', 'kor': 95, 'eng': 97, 'math': 99}, 
'name': 'Hojun', 'kor': 65, 'eng': 75, 'math': 60}, 
{'name': 'Yuna', 'kor': 78, 'eng': 82, 'math': 85}, 
{'name': 'Taeyang', 'kor': 92, 'eng': 89, 'math': 91}, 
{'name': 'Seojin', 'kor': 55, 'eng': 70, 'math': 68}]

'''






### 데이터 가공


# 평균
# (kor + eng + math) / 3
# 리스트 안의 딕셔너리에 접근하기 위해선
# 리스트 한줄씩 접근 > 점수들의 평균

# 새로운 컬럼을 만들어 평균을 저장한다

for i in students : 
    stu_avg = (i["kor"] + i["eng"] + i["math"]) / 3
    i["avg"] = stu_avg

# print(students)
'''
[{'name': 'Hannah', 'kor': 90, 'eng': 95, 'math': 85, 'avg': 90.0}, 
{'name': 'Minjun', 'kor': 80, 'eng': 88, 'math': 92, 'avg': 86.66666666666667}, 
{'name': 'Yujin', 'kor': 75, 'eng': 85, 'math': 100, 'avg': 86.66666666666667}, 
{'name': 'Dohyeok', 'kor': 100, 'eng': 70, 'math': 88, 'avg': 86.0}, 
{'name': 'Suyun', 'kor': 88, 'eng': 90, 'math': 93, 'avg': 90.33333333333333}, 
{'name': 'Jiwon', 'kor': 95, 'eng': 97, 'math': 99, 'avg': 97.0}, 
{'name': 'Hojun', 'kor': 65, 'eng': 75, 'math': 60, 'avg': 66.66666666666667}, 
{'name': 'Yuna', 'kor': 78, 'eng': 82, 'math': 85, 'avg': 81.66666666666667}, 
{'name': 'Taeyang', 'kor': 92, 'eng': 89, 'math': 91, 'avg': 90.66666666666667}, 
{'name': 'Seojin', 'kor': 55, 'eng': 70, 'math': 68, 'avg': 64.33333333333333}]

'''




# 합격 여부
# 합격(>=80) 불합격(<80)
# 리스트 한 줄에 접근 > 딕셔너리의 평균에 접근

# 리스트 안에 딕셔너리가 있는 형태이기 때문에 sum은 사용 불가능하겠구나
# 각각의 요소를 슬라이싱해서 더하고 과목만큼 나눠서 평균을 만들어야 하겠다

for i in students : 
    if i['avg'] >= 80 : 
        i['status'] = "합격"
    else : 
        i['status'] = "불합격"
print(students)
'''
[{'name': 'Hannah', 'kor': 90, 'eng': 95, 'math': 85, 'avg': 90.0, 'status': '합격'}, 
{'name': 'Minjun', 'kor': 80, 'eng': 88, 'math': 92, 'avg': 86.66666666666667, 'status': '합격'}, 
{'name': 'Yujin', 'kor': 75, 'eng': 85, 'math': 100, 'avg': 86.66666666666667, 'status': '합격'}, 
{'name': 'Dohyeok', 'kor': 100, 'eng': 70, 'math': 88, 'avg': 86.0, 'status': '합격'}, 
{'name': 'Suyun', 'kor': 88, 'eng': 90, 'math': 93, 'avg': 90.33333333333333, 'status': '합격'}, 
{'name': 'Jiwon', 'kor': 95, 'eng': 97, 'math': 99, 'avg': 97.0, 'status': '합격'}, 
{'name': 'Hojun', 'kor': 65, 'eng': 75, 'math': 60, 'avg': 66.66666666666667, 'status': '불합격'}, 
{'name': 'Yuna', 'kor': 78, 'eng': 82, 'math': 85, 'avg': 81.66666666666667, 'status': '합격'}, 
{'name': 'Taeyang', 'kor': 92, 'eng': 89, 'math': 91, 'avg': 90.66666666666667, 'status': '합격'}, 
{'name': 'Seojin', 'kor': 55, 'eng': 70, 'math': 68, 'avg': 64.33333333333333, 'status': '불합격'}]
'''



## for문이 중첩되기 때문에 모두 한번에 연산할 수 있음
# 각 단계를 print로 찍어보면서 단계적으로 접근한 뒤,
# 줄일 수 있다면 줄이는 것
for i in students : 
    i["kor"] = int(i["kor"]);
    i["eng"] = int(i["eng"]);
    i["math"] = int(i["math"]);

    stu_avg = (i["kor"] + i["eng"] + i["math"]) / 3
    i["avg"] = stu_avg

    if i['avg'] >= 80 : 
        i['status'] = "합격"
    else : 
        i['status'] = "불합격"

















