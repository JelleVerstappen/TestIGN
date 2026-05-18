select 
	ProcessParameterID,
	Assets.Description as assetName,
	Assets.AssetID,
	ProcessParameters.Description,
	DefaultValue,
	DefaultLowLow,
	DefaultLow,
	DefaultHigh,
	DefaultHighHigh,
	Unit,
	ProcessParameters.created,
	ProcessParameters.Modified,
	lines.Description as lineName,
	lines.lineID,
	tagPath
from
	ProcessParameters
left join 
	Assets
left join Lines on assets.lineID = lines.lineID
on
	ProcessParameters.AssetID = assets.AssetID
where ProcessParameters.active = 1
and (ProcessParameters.AssetID =  :assetID or  :assetID = -1)
and (assets.lineID =  :lineID or  :lineID = -1)
order by assetName asc, Description asc