SELECT date_format(DATETIME, '%H') HOUR, 
    count(ANIMAL_ID) 'COUNT'
FROM ANIMAL_OUTS
where date_format(DATETIME, '%H') between '09' and '19'
group by 1
order by 1
