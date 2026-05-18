select 
	assetID as value,
	description as label,
	AssetName
from
	assets
where
	LineID =  :lineID
	and
	active = 1