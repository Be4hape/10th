-- order_id, order_date, category, qty, price
-- SELECT category, sum(qty*price)
-- FROM sales
-- WHERE date_format(order_date, '%Y') = '2024'
-- group by category
-- order by (qty*price) desc


-- customers >> customer_id, name, city
-- orders    >> order_id, customer_id, order_date, amount
SELECT city, count(*) 'order_count', sum(amount) 'total_revenue'
FROM customers A
JOIN orders B on A.customer_id = B.customer_id
WHERE date_format(order_date, '%Y') = '2024'
group by city
order by sum(amount) desc, count(*) desc