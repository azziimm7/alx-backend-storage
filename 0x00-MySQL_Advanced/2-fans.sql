-- Count the number of fans in each county
SELECT origin, sum(fans) as nb_fans
       FROM metal_bands
       Group by origin
       ORDER BY nb_fans DESC;
