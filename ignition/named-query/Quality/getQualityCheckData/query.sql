select 
	QACheckData.*,
	Articles.ArticleNumber as Article,
	Articles.ArticleDescription as ArticleDescription,
	Lines.Description as Line
from
	QACheckData
left join
	Articles 
	on
	QACheckData.articleID = Articles.ArticleID
left join
	Lines
	on
	QACheckData.LineID = Lines.LineID
where QACheckData.active = 1
	and QACheckData.datetime between  :startDate and  :endDate 
	and (QACheckData.articleID =  :articleID or  :articleID = -1)
	and (QACheckData.LineID =  :LineID or  :LineID = -1)
	and (QACheckData.inspector =  :inspector or  :inspector = '-1')
order by datetime desc