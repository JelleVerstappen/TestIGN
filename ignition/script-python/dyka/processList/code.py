def loadProcessList(articleNumber, lineID):
	tagProvider = dyka.config.tagProvider
	parameters = {'articleNumber': articleNumber, 'lineID': lineID}
	articleParams = system.db.runNamedQuery('Article/ArticleManagement/getParamsBasedOnArticle', parameters)
	
	for row in range(articleParams.getRowCount()): # Loop over all parameters
		tagPath = articleParams.getValueAt(row, 'tagPath')
		
		if tagPath is not None:
			setpoint = articleParams.getValueAt(row, 'value')
			lowLimit = articleParams.getValueAt(row, 'low')
			highLimit = articleParams.getValueAt(row, 'high')
			lowLowLimit = articleParams.getValueAt(row, 'lowlow')
			highHighLimit = articleParams.getValueAt(row, 'highhigh')
			unit = articleParams.getValueAt(row, 'Unit')
			
			setpointPath = '[' + tagProvider + ']' + tagPath + '/Setpoint'
			lowLimitPath = '[' + tagProvider + ']' +  tagPath + '/Metadata/Low'
			highLimitPath = '[' + tagProvider + ']' + tagPath + '/Metadata/High'
			lowLowLimitPath = '[' + tagProvider + ']' + tagPath + '/Metadata/LowLow'
			highHighLimitPath = '[' + tagProvider + ']' + tagPath + '/Metadata/HighHigh'
			unitPath = '[' + tagProvider + ']' + tagPath + '/Metadata/Unit'
			
			tagPaths = [setpointPath, lowLimitPath, highLimitPath, lowLowLimitPath, highHighLimitPath, unitPath]
			values = [setpoint, lowLimit, highLimit, lowLowLimit, highHighLimit, unit]
			
			system.tag.writeBlocking(tagPaths, values)