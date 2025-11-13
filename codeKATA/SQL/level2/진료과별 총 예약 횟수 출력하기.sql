SELECT MCDP_CD '진료과코드',
    COUNT(distinct PT_NO) '5월예약건수'
FROM APPOINTMENT
WHERE DATE_FORMAT(APNT_YMD, '%Y-%m') = '2022-05'
GROUP BY 1
order by 2, 1

-- '2022년 5월에 예약한 환자 수' 라는 키워드는 5월에 예약된 모든 건이 아니라, 예약한 '환자의 수'가 키워드이기 때문에,
-- distinct를 사용해야 하는 것이 함정이었다. 유의해야함.
