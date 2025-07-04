SELECT
    u.id AS user_id,
    u.firstname || ' ' || u.lastname AS full_name,
    COUNT(c.id) AS total_orders,
    SUM(ci.quantity * p.price) AS total_spent
FROM users u
JOIN carts c ON u.id = c.user_id
JOIN cart_items ci ON c.id = ci.cart_id
JOIN products p ON ci.product_id = p.id
GROUP BY u.id, full_name
ORDER BY total_orders DESC
LIMIT 10;
