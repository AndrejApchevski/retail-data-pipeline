SELECT
    DATE(c.date) AS order_date,
    SUM(ci.quantity * p.price) AS total_revenue,
    COUNT(DISTINCT c.id) AS total_orders
FROM carts c
JOIN cart_items ci ON c.id = ci.cart_id
JOIN products p ON ci.product_id = p.id
GROUP BY DATE(c.date)
ORDER BY order_date;
