def solution(s):
    answer = ''

    return answer;

s = 'abcd'
char = list(s)
print(s)

# char[2] = 'x'
# s = "".join(char)
# print(s)

for i in range(len(s)) : 
    if(i % 2 == 0):
        char[i] = s[i].upper()

# 이 상태에선 리스트안에 각각의 문자 형태로 저장되어 있음
# 이를 문자열로 바꿔주어야 한다. > join
print(char)

# result에 char를 문자열 형태로 변경하여 저장, 이후 출력
result = "".join(char)
print(result)