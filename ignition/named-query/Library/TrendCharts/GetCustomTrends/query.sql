SELECT TrendChartID, TrendChartName
FROM TrendCharts
WHERE ((:TrendChartIsPrivate = 1 AND TrendChartIsPrivate = 1 AND UserID = :UserID)
	OR (:TrendChartIsPrivate = 0 AND TrendChartIsPrivate = 0))
	AND TrendChartID != 1
	AND Active = 1