SELECT SPProcedures.ProcedureID
      ,Lines.Description as Line
      ,SPProcedures.LineID
      ,Articles.ArticleNumber
      ,SPProcedures.ArticleID
      ,SPProcedures.Created
      ,SPProcedures.CreatedBy
      ,SPProcedures.Modified
      ,SPProcedures.ModifiedBy
FROM SPProcedures
Left join
	lines
	on
	SPProcedures.LineID = Lines.LineID
Left join
	Articles
	on
	SPProcedures.ArticleID = Articles.ArticleID
where SPProcedures.Active = 1
