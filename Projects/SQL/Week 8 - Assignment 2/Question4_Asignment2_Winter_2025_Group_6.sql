/*
GROUP 6 - Akash, Bruno and Edith - Assigment 2
Question 4
Develop a query to compute the interval, in days, between consecutive rentals for each customer
 in the Sakila database. The output should look like the followings:
rental_id 	customer_id 	rental_date           	days_until_next_rental
76        	1          	2005-05-25 11:30:37   	3
573       	1          	2005-05-28 10:35:23   	18
1185      	1          	2005-06-15 00:54:12   	0
1422      	1          	2005-06-15 18:02:53   	0
1476      	1          	2005-06-15 21:08:46   	1
*/

SELECT 
    r.rental_id,
    r.customer_id,
    r.rental_date,
    DATEDIFF( LEAD(r.rental_date) 
		OVER (PARTITION BY r.customer_id ORDER BY r.rental_date), 
		r.rental_date) AS days_until_next_rental
FROM sakila.rental r
ORDER BY r.customer_id, r.rental_date
