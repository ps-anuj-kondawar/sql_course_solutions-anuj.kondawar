WITH film_rentals AS (
    SELECT 
        c.name AS category,
        f.title,
        COUNT(r.rental_id) AS rentals
    FROM category c
    JOIN film_category fc ON c.category_id = fc.category_id
    JOIN film f ON fc.film_id = f.film_id
    LEFT JOIN inventory i ON f.film_id = i.film_id
    LEFT JOIN rental r ON i.inventory_id = r.inventory_id
    GROUP BY c.name, f.title
)
SELECT 
    category,
    title,
    rentals,
    RANK() OVER (PARTITION BY category ORDER BY rentals DESC) AS rnk
FROM film_rentals
ORDER BY category, rnk;
