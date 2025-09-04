/*   ******* 
GROUP 6 - Akash, Bruno and Edith - Assigment 2
Question 1 - Asignment2
Write a query that calculates the total number of rentals for each film in the Sakila database 
and partitions these films into quartiles based on their rental counts. 
Your result must include the film title, the total number of rentals, 
and the quartile number (1, 2, 3, or 4) for each film.
*/

SELECT 
	f.title, 
    COUNT(r.rental_id) AS rental_count,
    NTILE(4) OVER(ORDER BY count(r.rental_id)) AS film_quartile
FROM sakila.rental r 
JOIN sakila.inventory i 
	ON r.inventory_id = i.inventory_id
JOIN sakila.film f  
	ON i.film_id = f.film_id
GROUP BY f.film_id, f.title 
