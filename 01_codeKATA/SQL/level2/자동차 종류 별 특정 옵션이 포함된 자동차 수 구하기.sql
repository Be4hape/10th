SELECT CAR_TYPE, count(car_id) CARS
FROM CAR_RENTAL_COMPANY_CAR
WHERE (options like '%열선시트%') or (options like '%통풍시트%') or (options like '%가죽시트%')
group by car_type
order by car_type
