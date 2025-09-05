# Assigment 1 - CSPS - SQL Databases
# Group 6 - Akash, Bruno and Edith
#Question 2
# D)	Write a query using MySQL to return all countries that received their independence in the 18th century.
SELECT 
	Name,
    IndepYear
FROM world.country
WHERE IndepYear > 1700 AND IndepYear < 1801;