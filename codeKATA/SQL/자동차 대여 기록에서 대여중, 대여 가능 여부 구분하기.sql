SELECT CAR_ID,
    CASE WHEN car_id in(
        SELECT car_id 
        FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY
        WHERE '2022-10-16' BETWEEN start_date and end_date) then '대여중'
    else '대여 가능' end as 'AVAILABILITY'
FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY
group by car_id
order by car_id desc
