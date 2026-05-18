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
,	COUNT(*) cnt 
FROM
	alarm_events a
WHERE
	a.eventtime BETWEEN @startDate AND @endDate
	AND a.eventtype = 0
	AND a.source like @filter
GROUP BY
	a.displaypath 
ORDER BY
	cnt DESC, a.displaypath ASC
OFFSET 0 ROWS FETCH NEXT @limit ROWS ONLY