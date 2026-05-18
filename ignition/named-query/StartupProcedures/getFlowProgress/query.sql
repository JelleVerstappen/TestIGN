SELECT 
    CAST(
        SUM(CASE WHEN Status = 3 THEN 1 ELSE 0 END) * 100.0 
        / COUNT(*) 
        AS DECIMAL(5,2)
    ) AS CompletedPercentage
FROM SPStepLogging
where flowID = :flowID
GROUP BY FlowID;