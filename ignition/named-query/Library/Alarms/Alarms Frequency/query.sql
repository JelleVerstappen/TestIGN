SELECT top {limit}
	CASE WHEN a.displaypath = '' THEN 'Unknown' ELSE a.displaypath END displaypath, 	
	COUNT(*) cnt 
FROM 
	alarm_events a
WHERE 
	a.eventtime BETWEEN :startDate AND :endDate	AND a.eventtype = 0
GROUP BY 
	a.displaypath 
ORDER BY 
	cnt DESC, a.displaypath ASC 
