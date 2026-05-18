DECLARE @TargetNodeID INT = :targetNodeID ;

	;WITH ParentTree AS (
	    SELECT 
	        rn.RecipeElementID,
	        rn.ParentID,
	        0 AS Depth  -- start bij 0
	    FROM RecipeElements rn
	    WHERE rn.RecipeElementID = @TargetNodeID
	
	    UNION ALL
	
	    SELECT 
	        parent.RecipeElementID,
	        parent.ParentID,
	        pt.Depth + 1
	    FROM RecipeElements parent
	    INNER JOIN ParentTree pt ON pt.ParentID = parent.RecipeElementID
	),

	AllParams AS (
	    SELECT 
	        rp.RecipeElementID,
	        rn.Description AS NodeName,
	        rp.ProcessParameterValueID,
	        rp.ProcessParameterID,
	        rp.Value,
	        pc.Description,
	        pc.Unit,
	        pt.Depth,
	        pc.AssetID,
	        ROW_NUMBER() OVER (PARTITION BY rp.ProcessParameterID ORDER BY pt.Depth ASC) AS rn_order
	    FROM ParentTree pt
	    INNER JOIN ProcessParameterValues rp ON rp.RecipeElementID = pt.RecipeElementID
	    LEFT JOIN ProcessParameters pc ON pc.ProcessParameterID = rp.ProcessParameterID
	    LEFT JOIN RecipeElements rn ON rn.RecipeElementID = rp.RecipeElementID
	    where rp.active = 1
	)

	SELECT 
	    RecipeElementID,
	    NodeName,
	    ProcessParameterID,
	    ProcessParameterValueID,
	    Value,
	    AllParams.Description as ParamDesc,
	    Unit,
		Assets.Description as AssetDesc
	FROM AllParams
	left join Assets on AllParams.AssetID = Assets.AssetID
	WHERE rn_order = 1         -- alleen de "laagste" versie
	ORDER BY AllParams.Description