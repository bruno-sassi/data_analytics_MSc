/*
GROUP 6 - Akash, Bruno and Edith - Assigment 2
Question 5
Write a query to determine the top ten film categories by total rental count. 
Your output should include the film category name and the total number of rentals for that category. 
*/

SELECT
    c.name AS category_name,
    COUNT(r.rental_id) AS total_rentals
FROM
    sakila.category c
JOIN sakila.film_category fc ON c.category_id = fc.category_id
JOIN sakila.film f ON fc.film_id = f.film_id
JOIN sakila.inventory i ON f.film_id = i.film_id
JOIN sakila.rental r ON i.inventory_id = r.inventory_id
GROUP BY
    c.name
ORDER BY
    total_rentals DESC
LIMIT 10
