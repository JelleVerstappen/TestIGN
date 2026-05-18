select
	ArticleID,
	ArticleNumber,
	ArticleDescription,
	LinkedNodeID,
	Articles.LineID,
	Lines.Description as LineDesc,
	Articles.SawListID
from
	Articles
left join
	lines on articles.lineID = lines.lineID
where
	articles.active = 1
and
	(Articles.LineID =  :LineID or  :LineID = -1)
	