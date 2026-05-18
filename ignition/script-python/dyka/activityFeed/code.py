def addEntry(entryType, entryData):
	requiredDataDict = {'Comment': {
						'LineID': None,
						'Comment': None,
						'StatusID': None,
						'Article': None,
						'Datetime': None,
						'CreatedBy': None},
					'QualityRemark': {
						'LineID': None,
						'Comment': None,
						'Article': None,
						'Datetime': None,
						'CreatedBy': None},
					'SettingChange': {
						'LineID': None,
						'ProcessListNumber': None,
						'Comment': None,
						'Article': None,
						'Datetime': None,
						'CreatedBy': None},
					'ProgressUpdate': {
						'LineID': None,
						'ProgressType': None,
						'ProgressStatus': None,
						'Comment': None,
						'Article': None,
						'Datetime': None,
						'CreatedBy': None},
					'Alarm': {
						'LineID': None,
						'AlarmName': None,
						'Comment': None,
						'Article': None,
						'Datetime': None,
						'CreatedBy': None}}
	
	requiredData = requiredDataDict[entryType]
	
	for key in requiredData.keys():
		if key not in entryData.keys():
			print 'NOK'
			return
	
	if entryType == 'Comment':
		insertQuery = '''insert into 
								AFComments
							(LineID,
							 Comment,
							 StatusID,
							 Article,
							 CreationDate,
							 CreatedBy)
							values
								(?,
								 ?,
								 ?,
								 ?,
								 ?,
								 ?)'''
		insertArgs = [entryData['LineID'], entryData['Comment'], entryData['StatusID'],
					entryData['Article'], entryData['Datetime'], entryData['CreatedBy']]
	
	elif entryType == 'QualityRemark':
		insertQuery = '''insert into 
							AFQualityRemarks
						(LineID,
						 SampleNumber,
						 Article,
						 Comment,
						 CreationDate,
						 CreatedBy)
						values
							(?,
							 ?,
							 ?,
							 ?,
							 ?,
							 ?)'''
		insertArgs = [entryData['LineID'],entryData['Article'],entryData['Article'],
					entryData['Comment'],entryData['Datetime'],entryData['CreatedBy']]
	
	elif entryType == 'SettingsChange':
		insertQuery = '''insert into
							AFSettingsChange
						(LineID,
						 ProcessListNumber,
						 Comment,
						 Article,
						 CreationDate,
						 CreatedBy)
						values
							(?,
							 ?,
							 ?,
							 ?,
							 ?,
							 ?)'''
		insertArgs = [entryData['LineID'], entryData['Article'], entryData['Comment'],
					entryData['Article'], entryData['Datetime'], entryData['CreatedBy']]
	
	elif entryType == 'ProgressUpdate':
		insertQuery = '''insert into
							AFProgressUpdates
           				(LineID,
           				 ProgressType,
           				 ProgressStatus,
           				 Comment,
           				 Article,
           				 Creationdate,
           				 CreatedBy)
     					values
           					(?,
				           	 ?,
				           	 ?,
				           	 ?,
				           	 ?,
				           	 ?,
				           	 ?)'''
		insertArgs = [entryData['LineID'], entryData['ProgressType'], entryData['ProgressStatus'],
						entryData['Comment'], entryData['Article'], entryData['Datetime'], entryData['CreatedBy']]
	
	elif entryType == 'Alarm':
		insertQuery = '''insert into
							AFAlarms
						(LineID,
						 AlarmName,
						 Article,
						 CreatedBy,
						 CreationDate)
						values
							(?,
							 ?,
							 ?,
							 ?,
							 ?)'''
		insertArgs = [entryData['LineID'], entryData['AlarmName'], entryData['Article'],
						entryData['CreatedBy'], entryData['CreationDate']]
	
	system.db.runPrepUpdate(insertQuery, insertArgs, database = 'NLSTWDYK_DB_PROD')