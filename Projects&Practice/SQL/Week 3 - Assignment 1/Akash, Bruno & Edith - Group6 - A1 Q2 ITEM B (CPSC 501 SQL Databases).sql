# Assigment 1 - CSPS - SQL Databases
# Group 6 - Akash, Bruno and Edith
# Question 2
# B)	Write a query using MySQL that returns all countries in Europe.	
SELECT 
	Name
FROM world.country
WHERE country.continent = 'Europe'