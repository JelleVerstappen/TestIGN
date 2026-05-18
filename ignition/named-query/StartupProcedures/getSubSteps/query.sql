select
	*
from
	SPSubStepsConfig
left join
	SPSubStepLogging
on
	SPSubStepsConfig.SubStepID = SPSubStepLogging.SubStepID
and
	SPSubStepLogging.FlowID = :FlowID
where
	MainStepID =  :MainStepID
	and
	Active = 1