SELECT 
    JSON.[key]        AS label,
    cast(JSON_VALUE(JSON.value, '$.id') as int) AS value
FROM QASawList
	CROSS APPLY OPENJSON(config) AS JSON
WHERE active = 1;