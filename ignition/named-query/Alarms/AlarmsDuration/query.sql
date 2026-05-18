DECLARE
	@startDate DATETIME = :startDate
,	@endDate DATETIME = :endDate
,	@limit INT = :limit
,	@filter NVARCHAR(500) = replace(replace(:filter, '*', '%'), '?', '_');

SELECT
	CASE
		WHEN a.displaypath = '' THEN 'Unknown'
		ELSE a.displaypath
	END displaypath
,	SUM(datediff(SECOND, a.eventtime, COALESCE(c.eventtime, CURRENT_TIMESTAMP))) duration 
FROM
	alarm_events a 
	LEFT JOIN alarm_events c ON c.eventid = a.eventid AND c.eventtype = 1
WHERE
	a.eventtime BETWEEN @startDate AND @endDate
	AND a.eventtype = 0
	AND a.source like @filter
GROUP BY
	a.displaypath 
ORDER BY
	duration DESC, a.displaypath ASC 
OFFSET 0 ROWS FETCH NEXT @limit ROWS ONLY