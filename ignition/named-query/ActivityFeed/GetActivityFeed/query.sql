declare @line as nvarchar(MAX) = :line ;
declare @startDate as datetime2(0) = :startDate;
declare @endDate as datetime2(0) =  :endDate;
declare @ActivityType as nvarchar(MAX) = :activityType;
declare @commentStatus as int = :commentStatus;
declare @username as nvarchar(MAX) = :username ;

SELECT
	(
        SELECT 
            c.[CommentID],
            c.[LineID],
            lines.[Description] as lineName,
            c.[Comment],
            c.[CreatedBy],
            c.[CreationDate],
            c.[ParentCommentID],
            c.[StatusID],
            s.[Status],
            isnull(c.[Article], -1) as Article
        FOR JSON PATH, WITHOUT_ARRAY_WRAPPER
    ) AS [data],
            -- Subquery for Replies
            (
                SELECT 
                    r.[CommentID],
                    r.[LineID],
                    lines.description as lineName,
                    r.[Comment],
                    r.[CreatedBy],
                    r.[CreationDate],
                    r.[ParentCommentID],
                    r.[StatusID],
                    iif(r.[ImageBlob] is null, 0, 1) as hasImage,
                    rs.[Status]
                FROM [AFComments] r
                left JOIN AFcommentstatuses rs ON r.StatusID = rs.CommentStatusID
                left join lines on r.LineID = lines.LineID
                WHERE 
                    r.ParentCommentID = c.CommentID
                    AND r.Active = 1
                FOR JSON PATH
            ) AS Replies
			,'Comment' as [view],
			[CreationDate] as creationDate

        FROM [AFComments] c
        LEFT JOIN AFcommentstatuses s ON c.StatusID = s.CommentStatusID
        left join Lines on c.LineID = lines.LineID
        WHERE
                (@ActivityType = 'Comments' or @ActivityType = 'All')
				and
					(StatusID = @commentStatus or @commentStatus = -1)
				and
					(c.LineID = @line or @line = '-1')
				and 
					CreationDate between @startDate and @endDate
				and 
					c.active = 1
				and 
					c.ParentCommentID IS NULL
				AND (
					c.CreatedBy = @username
					OR EXISTS (
						SELECT 1
						FROM [AFComments] r
						WHERE 
							r.ParentCommentID = c.CommentID
							AND r.CreatedBy = @username 
							AND r.Active = 1
					)
					or @username = '-1'
				)
		
Union all
select (
	Select 
		[ProgressUpdateID]
      ,[AFProgressUpdates].[LineID]
      ,Lines.Description as lineName
      ,[ProgressType]
      ,[ProgressStatus]
      ,[Comment]
      ,[CreatedBy]
      ,[Creationdate]
      ,isnull([Article], -1) as Article
	for json path, WITHOUT_ARRAY_WRAPPER
	) as [data],
	Null as Replies,
	'Progress' as [view],
	[CreationDate] as creationDate
	from [AFProgressUpdates]
	left join lines on [AFProgressUpdates].lineID = lines.lineID
		where 
			(@ActivityType = 'Progress' or @ActivityType = 'All')
		and
			([AFProgressUpdates].LineID = @line or @line = '-1')
		and	
			CreationDate between @startDate and @endDate
		and 
			[AFProgressUpdates].active = 1
		
union all
select (
	Select 
		[QualityRemarkID]
		,[AFQualityRemarks].[LineID]
		,lines.description as lineName
      ,[SampleNumber]
      ,[Comment]
      ,[CreatedBy]
      ,[CreationDate]
      ,isnull([Article], -1) as Article
	for json path, WITHOUT_ARRAY_WRAPPER
	) as [data],
	Null as Replies,
	'QualityRemark' as [view],
	[CreationDate] as creationDate
	from [AFQualityRemarks]
	left join lines on [AFQualityRemarks].LineID = lines.lineID
		where
			(@ActivityType = 'Quality' or @ActivityType = 'All')
		and
			([AFQualityRemarks].lineID = @line or @line = '-1')
		and	
			CreationDate between @startDate and @endDate
		and 
			AFQualityRemarks.active = 1
		
union all
select (
	Select 
		[SettingsChangeID]
      ,[AFSettingsChanges].[LineID]
      ,lines.description as lineName
      ,[ProcessListNumber]
      ,[Comment]
      ,[CreatedBy]
      ,[CreationDate]
      ,isnull([Article], -1) as Article
	for json path, WITHOUT_ARRAY_WRAPPER
	) as [data],
	Null as Replies,
	'SettingChange' as [view],
	[CreationDate] as creationDate
	
	from [AFSettingsChanges]
	left join lines on [AFSettingsChanges].lineID = lines.lineID
		where
			(@ActivityType = 'Settings' or @ActivityType = 'All')
		and
			([AFSettingsChanges].LineID = @line or @line = '-1')
		and	
			CreationDate between @startDate and @endDate
		and 
			AFSettingsChanges.active = 1
		
union all
select (
	Select 
		[AlarmEntryID]
      ,[AFAlarms].[LineID]
      ,Lines.description as lineName
      ,[AlarmName]
      ,[Comment]
      ,[CreatedBy]
      ,[CreationDate]
      ,isnull([Article], -1) as Article
	for json path, WITHOUT_ARRAY_WRAPPER
	) as [data],
	Null as Replies,
	'Alarm' as [view],
	[CreationDate] as creationDate
	
	from [AFAlarms]
	left join lines on [AFAlarms].lineID = lines.lineID
		where
			(@ActivityType = 'Alarms' or @ActivityType = 'All')
		and
			([AFAlarms].LineID = @line or @line = '-1')
		and	
			CreationDate between @startDate and @endDate
		and 
			AFAlarms.active = 1

order by creationDate desc