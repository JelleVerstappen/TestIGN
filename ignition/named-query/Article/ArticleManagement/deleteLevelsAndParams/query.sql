SET XACT_ABORT ON;
BEGIN TRANSACTION;

DECLARE @RootID INT =  :rootID;
DECLARE @modifiedBy nvarchar(max) =  :modifiedBy;

;WITH ElementsToDeactivate AS (
    -- startnode
    SELECT RecipeElementID
    FROM RecipeElements
    WHERE RecipeElementID = @RootID

    UNION ALL

    SELECT re.RecipeElementID
    FROM RecipeElements re
    INNER JOIN ElementsToDeactivate etd
        ON re.ParentID = etd.RecipeElementID
)
SELECT RecipeElementID
INTO #ElementsToDeactivate
FROM ElementsToDeactivate
OPTION (MAXRECURSION 0);

CREATE INDEX IX_tmp_RecipeElementID ON #ElementsToDeactivate(RecipeElementID);

UPDATE re
SET re.Active = 0,
	re.modified = getdate(),
	re.modifiedBy = @modifiedBy
FROM RecipeElements re
INNER JOIN #ElementsToDeactivate d
    ON re.RecipeElementID = d.RecipeElementID;

UPDATE p
SET p.Active = 0,
	p.modified = getdate(),
	p.modifiedBy = @modifiedBy
FROM ProcessParameterValues p
INNER JOIN #ElementsToDeactivate d
    ON p.RecipeElementID = d.RecipeElementID;

COMMIT TRANSACTION;

DROP TABLE #ElementsToDeactivate;