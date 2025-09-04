/* 
GROUP 6 - Akash, Bruno and Edith - Assigment 2
Question 2
For each film category, write a query to identify the films with rental rates 
that exceed the average rental rate for that category. The output should display 
the film category name, film title, the film’s rental rate, and the average rental
 rate computed for the category.
 */
SELECT 
	category_name, 
    film_title, 
    film_rental_rate, 
    rental_avg_category  
FROM ( 
	SELECT 
		c.name AS category_name, 
        f.title AS film_title, 
        f.rental_rate AS film_rental_rate,
        AVG(f.rental_rate) OVER (PARTITION BY c.name) AS rental_avg_category 
	FROM sakila.film f  
	JOIN sakila.film_category fc 
		ON Fc.film_id=f.film_id
	JOIN sakila.category c 
		ON c.category_id=fc.category_id 
     ) y
WHERE y.film_rental_rate > rental_avg_category