select
	SawListID,
	VersionID,
	Config,
	CreatedBy,
	CreationDate
from 
	QASawList
where
	Active = 1