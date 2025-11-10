# # 입력 : 학생 점수, A-F 학점 계산
# def student_score (score):
#     if score >= 90:
#         return 'A'
#     elif score >= 80:
#         return 'B'
#     elif score >= 70:
#         return 'C'
#     elif score >= 60:
#         return 'D'
#     else : 
#         return 'F'

# score = int(input("점수 입력 : "))
# print("학점은 ", student_score(score), "이다.")



# 구구단 출력기
# 입력 : 숫자(2~9)

# def gugu(num):
#     if(not(9 >= num >= 2)):
#         return
#     else:
#         etr(num)

# def etr(nn):
#     for i in range(1, 10):
#         print('%d X %d = %d' %(nn, i, nn*i))

# print("출력하고 싶은 구구단 숫자 입력 : ")
# numnum = int(input())
# gugu(numnum)



# list 평균, 최대값 구하기
# def scores_analyze(scores):
#     avg_score = sum(scores) / len(scores)
#     max_score = max(scores)
#     return avg_score, max_score

# data = [80,90,100,12,34]
# avg, high = scores_analyze(data)
# print('평균 : %d, 최대값 : %d'%(avg, high))





#숫자 맞히기 게임
import random

answer = random.randint(1, 10) # random의 범위를 int형 1~10사이의 숫자로 지정
def guess_game(inin) : 
    if(inin == answer):
        print("correct!! You Win!")
        return 1;
    else : 
        print("You Lose..")
        return 0;


while True : 
    print("값 입력 : ")
    user_in = int(input())

    if guess_game(user_in) == 0:
        continue ; 
    elif guess_game(user_in) == 1:
        break;