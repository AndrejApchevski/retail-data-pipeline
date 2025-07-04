SELECT
    COUNT(DISTINCT c.id) AS total_carts,
    AVG(item_count) AS avg_items_per_cart,
    AVG(total_value) AS avg_cart_value
FROM (
    SELECT
        c.id AS cart_id,
        SUM(ci.quantity) AS item_count,
        SUM(ci.quantity * p.price) AS total_value
    FROM carts c
    JOIN cart_items ci ON c.id = ci.cart_id
    JOIN products p ON ci.product_id = p.id
    GROUP BY c.id
) AS cart_summary;
