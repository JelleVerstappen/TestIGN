DECLARE @articleNumber INT = :articleNumber;
DECLARE @lineNumber INT = :lineID;

WITH ParentTree AS (
    SELECT 
        rn.RecipeElementID,
        rn.ParentID,
        0 AS Depth
    FROM RecipeElements rn
    INNER JOIN Articles a
        ON rn.RecipeElementID = a.LinkedNodeID
    WHERE a.ArticleNumber = @articleNumber
      AND a.LineID = @lineNumber

    UNION ALL

    SELECT 
        parent.RecipeElementID,
        parent.ParentID,
        pt.Depth + 1
    FROM RecipeElements parent
    INNER JOIN ParentTree pt 
        ON pt.ParentID = parent.RecipeElementID
),

AllParams AS (
    SELECT
        pt.RecipeElementID,
        rn.Description AS NodeName,

        pp.ProcessParameterID,
        pp.Description AS ParamDesc,
        pp.Unit,
        pp.AssetID,

        pv.ProcessParameterValueID,
        pv.Value,
        pv.Low,
        pv.LowLow,
        pv.High,
        pv.HighHigh,

        pt.Depth,

        ROW_NUMBER() OVER (
            PARTITION BY pp.ProcessParameterID
            ORDER BY 
                CASE WHEN pv.ProcessParameterValueID IS NULL THEN 1 ELSE 0 END,
                pt.Depth
        ) AS rn_order
    FROM ParentTree pt
    CROSS JOIN ProcessParameters pp
    LEFT JOIN ProcessParameterValues pv
        ON pv.ProcessParameterID = pp.ProcessParameterID
       AND pv.RecipeElementID = pt.RecipeElementID
       AND pv.Active = 1
    LEFT JOIN RecipeElements rn
        ON rn.RecipeElementID = pt.RecipeElementID
   where pp.AssetID in (select AssetID from Assets where LineID = @LineNumber)
)

SELECT
    ap.RecipeElementID,
    ap.NodeName,
    ap.ProcessParameterID,
    ap.ProcessParameterValueID,

    -- default value als er geen override is
    COALESCE(ap.Value, pp.DefaultValue) AS Value,

    COALESCE(ap.Low, pp.DefaultLow) AS Low,
    COALESCE(ap.LowLow, pp.DefaultLowLow) as LowLow,
    COALESCE(ap.High, pp.DefaultHigh) as High,
    COALESCE(ap.HighHigh, pp.DefaultHighHigh) as HighHigh,

    ap.ParamDesc,
    ap.Unit,
    a.Description AS AssetDesc,
    pp.Tagpath
FROM AllParams ap
INNER JOIN ProcessParameters pp
    ON pp.ProcessParameterID = ap.ProcessParameterID
LEFT JOIN Assets a
    ON ap.AssetID = a.AssetID
WHERE ap.rn_order = 1
ORDER BY ap.ParamDesc;