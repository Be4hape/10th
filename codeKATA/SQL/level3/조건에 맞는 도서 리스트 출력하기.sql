SELECT BOOK_ID, date_format(PUBLISHED_DATE, '%Y-%m-%d') 'PUBLISHED_DATE'
FROM BOOK
WHERE date_format(published_date, '%Y') = '2021' and
    category = '인문'
ORDER BY 2
