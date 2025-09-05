# Assigment 1 - CSPS - SQL Databases
# Group 6 - Akash, Bruno and Edith
# Question 2
# C)	Write a query using MySQL to return all countries that speaks English as an official language with percentage greater than or equal to 70.
SELECT 
	country.Name
FROM world.countrylanguage
LEFT JOIN world.country ON countrylanguage.CountryCode = country.code
WHERE Language = 'English' AND IsOfficial = 'T' AND Percentage >=70;