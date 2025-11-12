'''
표준라이브러리
from 'where' import 'what'

import datetime
1. from datetime import * (다 가져오기)
2. from datetime import date, time, timedelta (특정 명령어만 가져온다)
> 특정 명령어를 가져오는 방식을 지향, 너무 많이 가져오면 손해


strftime > 날짜를 문자 형태로 저장
strptime > 날짜를 날짜 형태로 저장
"2025-11-12" ~ "2025-11-30" + 7 days를 하고 싶을 때 사용


d = date.today()
t = time(시, 분, 초)
dt = deltatime.now() #현재시간

gap = timedelta(days = 7, hours = 3) #timedelta로 시간을 더할 수 있음
>dt - timedelta(days=7) #이런식으로 사용






import math
math.pi, math.e
math.sqrt
math.pow



# math.pow와 x**y의 차이
x**y : 임의정밀도로 계산
math.pow : 항상 float 형태로 변환하여 반환한다. 값이 클수록 정밀도가 손실됨


임의 정밀도
(arbitrar - precision integer, bignum)
정수의 크기에 고정된 비트 수 한계가 없는 정수 타입.

필요한 만큼 메모리를 더 써서 정확한 값을 표현한다.

즉, float 형태로 바꾸는 math.pow는 자리수가 큰 값을 받게되면 15~17자리의 비트 수
만큼을 가지기 때문에 정밀도가 떨어질 수 있고,
임의정밀도의 값을 가지는 x**y는 자리수가 커져도 오버플로우가 일어나지 않아 정확하게
연산된다.
but, 그만큼 속도도 느려지는 것


### 파이썬 공식 문서
math.pow(x, y)
x의 y 거듭제곱을 반환합니다. 예외적인 경우는 최대한 IEEE 754 표준을 따릅니다. 
특히, x가 0이거나 NaN일 때도 pow(1.0, x)와 pow(x, 0.0)는 항상 1.0을 반환합니다.
 x 와 y가 모두 유한하고, x가 음수이고, y가 정수가 아니면 pow(x, y)는 정의되지 않고 ValueError를 발생시킵니다.

내장 ** 연산자와 달리, math.pow()는 두 인자를 모두 float 형으로 변환합니다. 
정확한 정수 거듭제곱을 계산하려면 **나 내장 pow() 함수를 사용하십시오.







import random
print(random.randint(1, 10)) # 1 ~ 10까지
print(random.randrange(0, 10, 2)) # 0, 2, 4, 6, 8






import os
os.getcwd  # 현재 작업 디렉토리
os.listdir # 현재 폴더의 항목 목록
os.path    # 독립경로

'''






