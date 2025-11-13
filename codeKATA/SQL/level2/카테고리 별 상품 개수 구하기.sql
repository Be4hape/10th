SELECT
    substr(product_code, 1, 2) CATEGORY,
    count(product_id) PRODUCTS
FROM PRODUCT
group by 1
order by 1
