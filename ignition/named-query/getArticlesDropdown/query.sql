select
	articleID as value,
	cast(articleNumber as nvarchar(max)) as label
from articles
where
	articles.active = 1
and lineID = :LineID