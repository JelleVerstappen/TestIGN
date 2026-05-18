SELECT 
	DATEPART(Hour,a.eventtime) label,
	COUNT(*) total,
	SUM(datediff(SECOND, a.eventtime, COALESCE(c.eventtime, CURRENT_TIMESTAMP))) duration 
FROM 
	alarm_events a 
		LEFT JOIN alarm_events c ON c.eventid = a.eventid AND c.eventtype = 1 
WHERE
	a.eventtime BETWEEN :startDate AND :endDate	AND a.eventtype = 0 
GROUP BY 
	DATEPART(Hour,a.eventtime)
ORDER BY
	DATEPART(Hour,a.eventtime) ASC