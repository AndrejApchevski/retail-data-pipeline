SELECT
    p.id AS product_id,
    p.title,
    SUM(ci.quantity) AS total_sold,
    COUNT(DISTINCT ci.cart_id) AS total_orders
FROM cart_items ci
JOIN products p ON ci.product_id = p.id
GROUP BY p.id, p.title
ORDER BY total_sold DESC
LIMIT 10;
