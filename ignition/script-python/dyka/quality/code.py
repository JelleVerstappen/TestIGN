testNameMapping = {
					"Diameter": "Diameter",
					"Height": "Hoogte",
					"MaxWallThickness": "Max. wanddikte",
					"MinWallThickness": "Min. wanddikte",
					"Shrink": "Krimp"}

def importFromCSV(path):
	text = system.file.readFileAsString(path,"UTF-8")
	rows = text.splitlines()
	
	# Start at index 1 to exclude header
	for i in range(1, len(rows)):
		row = rows[i]
		rawData = row.split(";")
		
		articleDescription = rawData[3]
		isDykaAir = True if 'AIR' in articleDescription else False
		if isDykaAir == True:
			print 'rowNumber ' + str(i)
			date = system.date.parse(rawData[0], 'dd-MM-yyyy')
			time = rawData[1]
			
			splitTime = time.split(':')
			
			hours = int(splitTime[0])
			minutes = int(splitTime[1])
			dateTime = system.date.setTime(date, hours, minutes, 0)
			
			productionDate = date
			
			articleNumber = rawData[2]
			articleID = system.db.runScalarPrepQuery('select articleID from articles where articleNumber = ?', [articleNumber], database = 'NLSTWDYK_DB_PROD')
			diameter = float(rawData[4].replace(',','.'))
			minWidth = float(rawData[5].replace(',','.'))
			maxWidth = float(rawData[6].replace(',','.'))
			shrink = float(rawData[7].replace(',','.'))
			
			hits = rawData[8]
			failedHits = rawData[9]
			failPercentage = rawData[10].replace(',','.')
			
			if len(failPercentage) == 0:
				failPercentage = 0
			try:
				failPercentage = float(failPercentage)
			except:
				failPercentage = 0
			hitsOK = 1 if failPercentage < 5 else 0
			
			height = float(rawData[11].replace(',','.'))
			printOK = 1 if rawData[12] == 'OK' else 0
			
			inspector = rawData[13]
			
			JSONstructArticle = system.util.jsonDecode(system.db.runScalarPrepQuery('select Checks from QAArticleSpecs where articleNumber =?', [articleNumber], database = 'NLSTWDYK_DB_PROD'))
			
			JSONstructArticle['MaxWallThickness']['Measured'] = maxWidth
			JSONstructArticle['HitsOK']['Measured'] = hitsOK
			JSONstructArticle['Shrink']['Measured'] = shrink
			JSONstructArticle['Height']['Measured'] = height
			JSONstructArticle['MinWallThickness']['Measured'] = minWidth
			JSONstructArticle['Diameter']['Measured'] = diameter
			JSONstructArticle['PrintOK']['Measured'] = printOK
			
			# Calculate if approved
			approved = True
			for itemName in JSONstructArticle:
				item =  JSONstructArticle[itemName]
				try:
					if item["Measured"] == '':
						continue
					if float(item["Measured"]) < float(item["LowLimit"]) or float(item["Measured"]) > float(item["HighLimit"]):
						item["ResultGood"] = False
						approved = False
						break
				except:
					continue
			
			insertQuery = '''insert into QACheckData
								([Datetime]
								,[LineID]
								,[ArticleID]
								,[ArticleDescription]
								,[TimeOnTube]
								,[Results]
								,[Approved]
								,[Inspector]
								,[Operator]
								,[ProductionDate])
							VALUES
							(?
							,?
							,?
							,?
							,?
							,?
							,?
							,?
							,?
							,?)'''
			args = [dateTime, 1, articleID, articleDescription, time, system.util.jsonEncode(JSONstructArticle), approved, inspector, None, date]
			system.db.runPrepUpdate(insertQuery, args, database = 'NLSTWDYK_DB_PROD')
		
	importFromCSV('C:\\AT\\CSV PKB 2025 Dyka Air lijn 7.csv')