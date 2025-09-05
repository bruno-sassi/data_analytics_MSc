# Assigment 1 - CSPS - SQL Databases
# Group 6 - Akash, Bruno and Edith
# Question 2
# E)	Write a query using MySQL that returns the following dataset. (Image on file with 12 City names, all with country code = IND and District = Delhi or Punjab)
SELECT
	Name,
    CountryCode,
    District
FROM world.city
WHERE CountryCode = 'IND' AND District IN ('Delhi', 'Punjab')
