-- Selects customer details along with their geographic information using a LEFT JOIN on GeographyID
SELECT
    c.CustomerID,
    c.CustomerName,
    c.Email,
    c.Gender,
    c.Age,
    g.Country,
    g.City
FROM 
    dbo.customers AS c
LEFT JOIN
    dbo.geography AS g
ON
    c.GeographyID = g.GeographyID;
