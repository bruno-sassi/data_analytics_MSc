-- **/* Question 2 from assignment for SQL DATABASE */

-- ** A)	Write a query using MySQL to return all countries included in the World database.
SELECT 
	Name
FROM world.country

-- ** B)	Write a query using MySQL that returns all countries in Europe.

SELECT 	Name FROM world.country
WHERE country.continent = 'Europe'

-- ** C)	Write a query using MySQL to return all countries that speaks English as an official language with percentage greater than or equal to 70.

SELECT c.name as Country FROM world.country c
left join world.countrylanguage c1
ON c.code=c1.CountryCode 
where c1.language='English' and c1.isofficial='T' and c1.Percentage >= 70 

-- ** D)	Write a query using MySQL to return all countries that received their independence in the 18th century.
SELECT 	Name, IndepYear
FROM world.country
WHERE IndepYear > 1700 AND IndepYear < 1801;

-- ** E)	Write a query using MySQL that returns the following dataset.
SELECT Name, CountryCode,	District
FROM world.city
WHERE CountryCode = 'IND' AND District IN ('Delhi', 'Punjab')


