WITH getTopFlowID AS (
    SELECT MAX(SPFlowLogging.FlowID) AS maxFlowID
    FROM SPFlowLogging
    WHERE SPFlowLogging.ProcedureID = :ProcedureID
)

SELECT 
    SPMainStepsConfig.StepID,
    SPMainStepsConfig.Name,
    SPFlowLogging.LineID,
    SPFlowLogging.ArticleID,
    SPStepLogging.Started,
    SPStepLogging.Completed,
    SPStepLogging.CompletedBy,
    ISNULL(SPStatusTypes.Name, 'TO DO') AS Status
FROM SPMainStepsConfig

LEFT JOIN SPFlowLogging
    ON SPMainStepsConfig.ProcedureID = SPFlowLogging.ProcedureID
   AND SPFlowLogging.FlowID = (SELECT maxFlowID FROM getTopFlowID)

LEFT JOIN SPStepLogging
    ON SPFlowLogging.FlowID = SPStepLogging.FlowID
   AND SPMainStepsConfig.StepID = SPStepLogging.StepID

LEFT JOIN SPStatusTypes
    ON SPStepLogging.Status = SPStatusTypes.StatusID

WHERE 
    SPMainStepsConfig.ProcedureID = :ProcedureID
    AND SPMainStepsConfig.Active = 1
