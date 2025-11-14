SELECT ORDER_ID, PRODUCT_ID, date_format(OUT_DATE, '%Y-%m-%d') 'OUT_DATE',
    CASE WHEN DATE_FORMAT(OUT_DATE, '%Y-%m-%d') <= '2022-05-01' then '출고완료'
        WHEN DATE_FORMAT(OUT_DATE, '%Y-%m-%d') > '2022-05-01' then '출고대기'
        else '출고미정' end as '출고여부'
FROM FOOD_ORDER
ORDER BY ORDER_ID
