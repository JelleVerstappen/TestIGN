select 
	QALineCheckData.Datetime,
	QALineCheckData.LineID,
	QALineCheckData.Results,
	QALineCheckData.Approved,
	QALineCheckData.OperatorName, 
	Articles.ArticleNumber as Article,
	Articles.ArticleDescription as ArticleDescription,
	Lines.Description as Line,
	QALineCheckData.ArticleID
from
	QALineCheckData
left join
	Articles 
	on
	QALineCheckData.articleID = Articles.ArticleID
left join
	Lines
	on
	QALineCheckData.LineID = Lines.LineID
where 
(QALineCheckData.Datetime between :startDate and :endDate)
and (QALineCheckData.lineID = :lineID or :lineID = -1)
and (QALineCheckData.articleID = :articleID or :articleID = -1)
and (QALineCheckData.OperatorName =  :inspector or  :inspector = '-1')
and QALineCheckData.active = 1