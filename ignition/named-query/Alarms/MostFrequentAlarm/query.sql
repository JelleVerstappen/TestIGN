DECLARE @filter NVARCHAR(500) = replace(replace(:filter, '*', '%'), '?', '_');

SELECT top 1
	CASE WHEN a.displaypath = '' THEN 'Unknown' ELSE a.displaypath END displaypath, 
	COUNT(*) total 
FROM 
	alarm_events a 
WHERE 	
	a.eventtime BETWEEN :startDate AND :endDate
	AND a.eventtype = 0
	AND a.source like @filter
GROUP BY
	a.displaypath 
ORDER BY total DESC 
