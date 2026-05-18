SELECT top 1
	CASE WHEN a.displaypath = '' THEN 'Unknown' ELSE a.displaypath END displaypath, 
	COUNT(*) total 
FROM 
	alarm_events a 
WHERE 	
	a.eventtime BETWEEN :startDate AND :endDate	AND a.eventtype = 0
GROUP BY
	a.displaypath 
ORDER BY total DESC 
