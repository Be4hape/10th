SELECT distinct A.car_id
FROM CAR_RENTAL_COMPANY_CAR A
JOIN CAR_RENTAL_COMPANY_RENTAL_HISTORY B ON A.car_id = B.car_id
WHERE car_type = '세단' and
    date_format(start_date, '%Y-%m') = '2022-10'
order by 1 desc
