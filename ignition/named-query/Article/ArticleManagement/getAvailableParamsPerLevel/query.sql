Declare @RecipeElementID int = :recipeElementID;

SELECT 
  p.ProcessParameterID AS value,
  p.description AS label
FROM 
  ProcessParameters p
  LEFT JOIN Assets a ON p.AssetID = a.AssetID
WHERE 
  a.LineID = (
    SELECT re.LineID
    FROM RecipeElements re
    WHERE re.RecipeElementID = @RecipeElementID
  )
  AND p.description NOT IN (
    SELECT 
      pp.description
    FROM
      ProcessParameterValues ppv
      LEFT JOIN RecipeElements re2 ON ppv.RecipeElementID = re2.RecipeElementID
      LEFT JOIN ProcessParameters pp ON ppv.ProcessParameterID = pp.ProcessParameterID
    WHERE 
      re2.RecipeElementID = @RecipeElementID
      AND ppv.active = 1
  );