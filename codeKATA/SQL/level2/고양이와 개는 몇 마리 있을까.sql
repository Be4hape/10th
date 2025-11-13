SELECT ANIMAL_TYPE, 
    count(ANIMAL_ID) as 'count'
FROM ANIMAL_INS
group by 1
order by 1
