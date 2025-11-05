# 11.05. 원유선 튜터님 - 흐름, 제어
# 조건문, 반복문, 둘의 결합
# debugging은 터미널에서 'python 파일명' 으로 가능


# 파이썬 나누기 연산자 : /, //, %
# / : 몫이 소수점 형태로 나옴.
# // : 몫이 정수 형태로
# % : 나머지


# 1. 조건문 - 파이썬은 elif 사용
'''
if 조건 : 
    실행문1
elif 조건2 : 
    실행문2
else : 
    그 외 실행문
'''

# while True : 
#     a = int(input("숫자 입력: "))
#     if(a % 2 == 1):
#         print("홀수")
#     elif(a % 2 == 0):
#         if(a == 0):
#             print("roop exit")
#             break;
#         print("짝수")
#     else : 
#         print("잘못된 입력")




# 2. 반복문
'''
for i in range() : 
    실행문
for i in j:
    실행문
> j는 순환 가능한 객체


for문 내부구조 (대충 표현): 
typedef struct {
    PyObject_HEAD
    PyListObject *list;   // 실제 리스트 객체
    Py_ssize_t index;     // 현재 위치 (0, 1, 2, ...)
} listiterobject;
1. for x in some_list가 시작
2. python은 pyobject_getiter(some_list)를 호출해서 list ierator 객체를 만듦
3. next(iterator)를 부를 때마다 내부에서 list -> ob_item[index] 이런식으로 C레벨 배열 접근
4. index를 1씩 올려간다.
5. 위 과정 반복

> 따라서 for i in j 같은 형식으로 사용할 때에, 리스트, 튜플, 딕셔너리가 들어간다면
  인덱스를 활용해서 반복하는 것임.

*for문이 인덱스를 직접 돌지 않는다, 타입 전용 iterator가 내부 인덱스를 하나 들고 +1씩 올려가며 돈다.


마찬가지로, range(시작, 끝, step)도 itorator 내부에서 숫자를 하나 들고 다니면서
current += step 형태로 동작하는 것.


Q : 기준이 인덱스인가? 
A : 언어레벨에선 아니다. but, 구현 레벨에서는 리스트/튜플/문자열 같은 시퀀스의 iterator 내부는 인덱스를 들고 돈다.



while 조건 : 
    실행문

'''

for i in range(1, 6):
    print(" " * (5 - i), "*"*i)












