/*
GROUP 6 - Akash, Bruno and Edith - Assigment 2
Question 3
Create a query that ranks films within each language by their replacement cost in descending order. 
Your result should include the film title, the language, the replacement cost, 
and the rank of each film within its language group. */

SELECT 
	f.title, 
    l.name, 
    f.replacement_cost, 
    RANK() OVER (ORDER BY f.replacement_cost DESC) AS rank_film_by_cost
FROM  sakila.film f  
JOIN sakila.language l 
	ON l.language_id = f.language_id
