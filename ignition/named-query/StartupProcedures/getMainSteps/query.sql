SELECT StepID
      ,ProcedureID
      ,SequenceNumber
      ,Name
      ,Created
      ,CreatedBy
      ,Modified
      ,ModifiedBy
      , count(SPSubStepsConfig.SubStepID) as SubStepCount
FROM 
	SPMainStepsConfig
LEFT JOIN
    SPSubStepsConfig
ON
    SPMainStepsConfig.StepID = SPSubStepsConfig.MainStepID and SPSubStepsConfig.Active = 1
where
	SPMainStepsConfig.Active = 1
	and
	SPMainStepsConfig.ProcedureID = :ProcedureID
group by
    StepID,
    ProcedureID,
    SequenceNumber,
    Name,
    Created,
	CreatedBy,
    Modified,
    ModifiedBy
order by SequenceNumber
