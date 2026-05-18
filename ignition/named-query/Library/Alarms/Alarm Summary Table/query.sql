SELECT  
	(CASE a.priority 
		WHEN 1 THEN 'Low'
		WHEN 2 THEN 'Medium'
		WHEN 3 THEN 'High'
		WHEN 4 THEN 'Critical'
		ELSE 'Diagnostic'
	END) as Priority,
	SUM(CASE WHEN c.eventtime IS NULL THEN 1 ELSE 0 END) active,
	SUM(CASE WHEN c.eventtime IS NULL THEN 0 ELSE 1 END) cleared,
	SUM(CASE WHEN k.eventtime IS NULL THEN 1 ELSE 0 END) unacknowledged, 
	COUNT(*) total,
	AVG(CASE WHEN k.eventtime IS NULL THEN 0 ELSE datediff(SECOND, a.eventtime, COALESCE(k.eventtime, CURRENT_TIMESTAMP)) END) acknowledgeTime, 
	AVG(CASE WHEN c.eventtime IS NULL THEN 0 ELSE datediff(SECOND, a.eventtime, COALESCE(c.eventtime, CURRENT_TIMESTAMP)) END) clearTime, 
	SUM(CONVERT(bigint,datediff(SECOND, a.eventtime, COALESCE(c.eventtime, CURRENT_TIMESTAMP)))) totalTime 
	--SUM(datediff(SECOND, a.eventtime, COALESCE(c.eventtime, CURRENT_TIMESTAMP))) totalTime 
FROM 
	alarm_events a  
		LEFT JOIN alarm_events c ON c.eventid = a.eventid AND c.eventtype = 1  
		LEFT JOIN alarm_events k ON k.eventid = a.eventid AND k.eventtype = 2
WHERE 
	a.eventtime 
		BETWEEN :startDate AND :endDate
	AND a.eventtype = 0
GROUP BY 
	a.priority
ORDER BY  
	a.priority ASC