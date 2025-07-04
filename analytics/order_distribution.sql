SELECT
    EXTRACT(HOUR FROM c.date) AS hour,
    COUNT(*) AS orders_count
FROM carts c
GROUP BY hour
ORDER BY hour;
