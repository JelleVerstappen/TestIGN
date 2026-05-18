	WITH RecipeTree AS (
	    -- Anchor: start bij de root
	    SELECT 
	        rn.RecipeElementID,
	        rn.ParentID,
	        rn.Description,
	        1 AS Level,
	        rn.lineID,
	        CAST(RIGHT('0000' + CAST(rn.RecipeElementID AS VARCHAR(4)), 4) AS VARCHAR(MAX)) AS PathIDsForSort, -- start van het pad
	        CAST(rn.RecipeElementID AS VARCHAR(MAX)) AS PathIDs  -- start van het pad
	    FROM RecipeElements rn
	    WHERE rn.ParentID IS NULL and rn.active = 1
	
	    UNION ALL
	
	    -- Recursive: pak de kinderen en bouw het pad op
	    SELECT 
	        child.RecipeElementID,
	        child.ParentID,
	        child.Description,
	        rt.Level + 1,
	        child.lineID,
	        CAST(rt.PathIDsForSort + ',' + RIGHT('0000' + CAST(child.RecipeElementID AS VARCHAR(4)), 4) AS VARCHAR(MAX)) AS PathIDsForSort,
	        CAST(rt.PathIDs + ',' + CAST(child.RecipeElementID AS VARCHAR(MAX)) AS VARCHAR(MAX)) AS PathIDs
	    FROM RecipeElements child
	    INNER JOIN RecipeTree rt
	        ON child.ParentID = rt.RecipeElementID
	        and child.active = 1
	)

	, RevParams as (
	Select 
	    ProcessParameterValues.RecipeElementID
	,   ProcessParameterValues.ProcessParameterID
	,   ProcessParameterValues.ProcessParameterValueID
	,   isnull(ProcessParameterValues.Value, ProcessParameters.DefaultValue) as value
	,	isnull(ProcessParameterValues.LowLow, ProcessParameters.DefaultLowLow) as LowAlarm
	,	isnull(ProcessParameterValues.Low, ProcessParameters.DefaultLow) as LowWarning
	,	isnull(ProcessParameterValues.High, ProcessParameters.DefaultHigh) as HighWarning
	,	isnull(ProcessParameterValues.HighHigh, ProcessParameters.DefaultHighHigh) as HighAlarm
	,	isnull(ProcessParameters.unit, '') as unit
	,   ProcessParameters.Description
	,   RecipeElements.Description as levelDesc
	from ProcessParameterValues
	left join ProcessParameters
	on ProcessParameterValues.ProcessParameterID = ProcessParameters.ProcessParameterID
	left join RecipeElements
	on ProcessParameterValues.RecipeElementID = RecipeElements.RecipeElementID
	where ProcessParameterValues.active = 1
	)
	
	SELECT 
	    rt.Level,
	    rt.PathIDs,
		rt.Description,
	    rt.ParentID,
	    rt.PathIDsForSort,
	    rt.RecipeElementID,
	    rt.lineID,
	    Articles.ArticleNumber,
	    Articles.ArticleID,
	    -- JSON van alle parameters voor deze node
	    (
	        SELECT 
	            rp.ProcessParameterID,
	            rp.ProcessParameterValueID,
	            rp.Value,
--	            rp.LowAlarm,
--	            rp.LowWarning,
--	            rp.HighWarning,
--	            rp.HighAlarm,
	            CAST(ABS(rp.LowAlarm - rp.value) AS DECIMAL(5,2)) LowAlarm,
	            CAST(ABS(rp.LowWarning - rp.value) AS DECIMAL(5,2)) LowWarning,
	            CAST(ABS(rp.HighWarning - rp.value) AS DECIMAL(5,2)) HighWarning,
	            CAST(ABS(rp.HighAlarm - rp.value) AS DECIMAL(5,2)) HighAlarm,
	            rp.Description,
	            rp.Unit
	        FROM RevParams rp
	        WHERE rp.RecipeElementID = rt.RecipeElementID
            ORDER BY Description
	        FOR JSON PATH
	    ) AS ParametersJSON
	FROM RecipeTree rt
	left join Articles
		on rt.RecipeElementID = Articles.LinkedNodeID
		and rt.lineID = Articles.lineID and Articles.active = 1
	ORDER BY rt.PathIDsForSort;