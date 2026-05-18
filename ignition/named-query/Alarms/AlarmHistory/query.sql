DECLARE @filter NVARCHAR(500) = replace(replace(:filter, '*', '%'), '?', '_');

SELECT top :limit
	e.eventTime eventTime, 
	e.displayPath, 
	dbo.SUBSTRING_INDEX(source, '/alm:', -1) name,
	e.eventType,
	CASE WHEN e.priority = 0 THEN 'Diagnostic' WHEN e.priority = 1 THEN 'Low' WHEN e.priority = 2 THEN 'Medium' WHEN e.priority = 3 THEN 'High' WHEN e.priority = 4 THEN 'Critical' ELSE '' END priority,
	COALESCE(COALESCE(COALESCE(d.intvalue, d.floatvalue), d.strvalue), '') eventValue,
	COALESCE(ack.strvalue, '') ackUser
FROM 
	alarm_events e 
		LEFT JOIN alarm_event_data d ON d.id = e.id AND d.propname = 'eventValue' 
		LEFT JOIN alarm_event_data ack ON ack.id = e.id AND ack.propname = 'ackUser'
WHERE 
	eventtime BETWEEN :startDate AND :endDate AND priority BETWEEN :minPriority AND :maxPriority AND
	((:active = 1 AND e.eventtype = 0) OR (:clear = 1 AND e.eventtype = 1) OR (:ack = 1 AND e.eventtype = 2))
	AND a.source like @filter
ORDER BY 
	e.eventTime DESC
 