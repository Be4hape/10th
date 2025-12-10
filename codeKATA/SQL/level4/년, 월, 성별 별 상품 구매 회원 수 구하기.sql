SELECT date_format(sales_date, '%Y') 'YEAR', date_format(sales_date, '%m') 'MONTH', GENDER, count(DISTINCT A.user_id) 'USERS'
FROM USER_INFO A
JOIN ONLINE_SALE B ON A.user_id = B.user_id
WHERE GENDER IS NOT NULL
group by 1, 2, 3
order by 1, 2, 3
