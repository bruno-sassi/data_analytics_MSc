# Assigment 1 - CPSC 501 - SQL Databases
# Group 6 - Akash, Bruno and Edith
# Question 2

USE world;

# A)	Write a query using MySQL to return all countries included in the World database.
SELECT 
	Name 
FROM world.country;

# B)	Write a query using MySQL that returns all countries in Europe.
SELECT 
	Name 
FROM country 
WHERE Continent = 'Europe';

# C)	Write a query using MySQL to return all countries that speaks English as an official language with percentage greater than or equal to 70.
SELECT c.Name 
FROM country c
JOIN countrylanguage cl ON c.Code = cl.CountryCode
WHERE cl.Language = 'English' AND cl.IsOfficial = 'T' AND cl.Percentage >= 70;

# D)	Write a query using MySQL to return all countries that received their independence in the 18th century.
SELECT 
	Name, 
	IndepYear 
FROM country 
WHERE IndepYear BETWEEN 1701 AND 1800;

# E)	Write a query using MySQL that returns the following dataset.
SELECT 
	Name, 
    CountryCode, 
    District 
FROM city 
WHERE CountryCode = 'IND' 
AND District IN ('Delhi', 'Punjab');