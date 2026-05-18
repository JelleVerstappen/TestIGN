import time
def joinIndexed(ds1,ds2,joinColumns,joinType='inner', over50k=False):
	"""
	Function to join to datasets together in an efficient way by creating an index. 
	Will work for 'inner' and 'left' joins. 

	Args:
		ds1 (dataset): The first dataset to join on.
		ds2 (dataset): The second dataset to join.
		joinColumns (list): List of columns that must match across both datasets to successfully join.
		joinType (string): Dictates whether to perform an inner or left join.
		over50k (boolean): defualt is False. Set to true if dataset contains more than 50k rows. Will take longer to join.
	Returns:
		The joined dataset.
	"""
	###logger
	logger = ata.scriptconsole.getLogger("DatasetJoin")
	
	startTime = time.time()
	pyColHeader1 = system.dataset.getColumnHeaders(ds1)
	pyColHeader2 = system.dataset.getColumnHeaders(ds2)
	
	pyDS1 = system.dataset.toPyDataSet(ds1)
	pyDS2 = system.dataset.toPyDataSet(ds2)
	# Iterate the datasets and index the data
	# store the joinCol values and a list of indexes where they are found
	dsIndex1 = {}
	dsIndex2 = {}
	
	if (len(pyDS1) > 50000 or len(pyDS2) > 50000) and not over50k:
		system.gui.messageBox("Overflow flag required, datasets exceed 50k rows")
		return
	
	# Create an index map for ds1 and ds2
	# this ends up looking like {(key1,key2):[rowIndex1,rowIndex2..]}
	# the keys represent the matching columns so I can build a
	# lightweight map of which rows have the same keys
	for i,row in enumerate(pyDS1):
		colKeys =()
		for colnames in joinColumns:
			colKeys+=(row[colnames],)
		# save the index with the IndexDicts
		dsIndex1[colKeys] = dsIndex1.get(colKeys,[])+[i]

	for i,row in enumerate(pyDS2):
		colKeys =()
		for colnames in joinColumns:
			colKeys+=(row[colnames],)
		# save the index with the IndexDicts
		dsIndex2[colKeys] = dsIndex2.get(colKeys,[])+[i]		
	
	# I go over dsIndex1 first and attempt to match each colkey to 	
	# ds2Index
	# If I can locate it I have a match
	# Otherwise I discard the entire row.
	allRows = []
	if joinType == "inner":
		for k,v in dsIndex1.iteritems():
			for rowIdx1 in v:
				oneRow = []
				for rowIdx2 in dsIndex2.get(k,[]):
					oneRow = list(pyDS1[rowIdx1]) + list(pyDS2[rowIdx2])
					if len(oneRow) == len(pyColHeader1 + pyColHeader2):
						allRows.append(oneRow)			
	
	elif joinType == "left":		
		blankDS2List = [None for i in pyColHeader2]

		for k,v in dsIndex1.iteritems():
			for rowIdx1 in v:
				for rowIdx2 in dsIndex2.get(k,[]):
					oneRow = list(pyDS1[rowIdx1])	
					allRows.append(oneRow + list(pyDS2[rowIdx2]))		
				if len(dsIndex2.get(k,[])) == 0:
					oneRow = list(pyDS1[rowIdx1])
					allRows.append(oneRow+blankDS2List)
	msg = "Optimized %s duration: "%joinType, time.time()-startTime
	logger.info(str(msg))
	return system.dataset.toDataSet(pyColHeader1+pyColHeader2, allRows)	

def formatMinutes(dataset, columnName, returnColumnName='FormattedDuration',noMinutes=False):
    """
    Formats the minutes in the specified column of the dataset into HH:MM:00 format.

    Args:
        dataset: The input dataset.
        columnName: The name of the column containing minutes to be formatted.
        returnColumnName: (Optional) The name of the new column to store formatted values.
        noMinutes: bool (Optional) Will take the minutes of the string
        
    Returns:
        The dataset with the new column containing formatted duration.
    """
    formattedChangeoverTimeRows = []

    for row in system.dataset.toPyDataSet(dataset):
        changeoverTime = row[columnName]
        if changeoverTime is not None:
			hours, minutes = divmod(changeoverTime, 60)
			if noMinutes:
				formattedChangeoverTimeRows.append('{:02d}:{:02d}'.format(int(hours), int(minutes)))
			else:
				formattedChangeoverTimeRows.append('{:02d}:{:02d}:00'.format(int(hours), int(minutes)))
        else:
            formattedChangeoverTimeRows.append('')

    return system.dataset.addColumn(dataset, formattedChangeoverTimeRows, returnColumnName, str)


def formatSeconds(dataset, columnName, returnColumnName='FormattedDuration',noMinutes=False):
    """
    Formats the seconds in the specified column of the dataset into HH:MM:SS format.

    Args:
        dataset: The input dataset.
        columnName: The name of the column containing seconds to be formatted.
        returnColumnName: (Optional) The name of the new column to store formatted values.
        noMinutes: bool (Optional) Will take the minutes of the string

    Returns:
        The dataset with the new column containing formatted duration.
    """
    formattedChangeoverTimeRows = []

    for row in system.dataset.toPyDataSet(dataset):
        changeoverTime = row[columnName]
        if changeoverTime is not None:
            hours, remainder = divmod(changeoverTime, 3600)
            minutes, seconds = divmod(remainder, 60)
            if noMinutes:
            	formattedChangeoverTimeRows.append('{:02d}:{:02d}'.format(int(hours), int(minutes)))
            else:
            	formattedChangeoverTimeRows.append('{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds)))
        else:
            formattedChangeoverTimeRows.append('')
		
			
    return system.dataset.addColumn(dataset, formattedChangeoverTimeRows, returnColumnName, str)


def datasetToList(dataset):
    """
    Converts a dataset into a list of dictionaries, where each dictionary represents a row.

    Args:
        dataset: The input dataset.

    Returns:
        list: A list of dictionaries representing the dataset rows.
    """
    return [{column: dataset.getValueAt(row, column) for column in dataset.getColumnNames()} for row in range(dataset.getRowCount())]


def datasetToJSON(dataset):
    """
    Converts a dataset into a JSON-formatted string.

    Args:
        dataset: The input dataset.

    Returns:
        str: A JSON-formatted string representing the dataset.
    """
    return system.util.jsonEncode(datasetToList(dataset))

def datasetFromJSON(jsonData):
    """
    Converts a list of dictionaries (JSON data) into a dataset.

    Args:
        json_data (list): A list of dictionaries representing the JSON data.

    Returns:
        com.inductiveautomation.ignition.common.Dataset: The resulting dataset.
    """
    try:
        # Extract column names from the keys of the first dictionary in the list
        columns = dict(jsonData[0]).keys()
        data = []

        for item in jsonData:
            row = []

            # Iterate through columns and retrieve cell values from the dictionary
            for column in columns:
                cellValue = item.get(column, '')

                try:
                    # Attempt to unpack nested dictionary and retrieve 'value' key
                    cellValue = dict(cellValue)['value']
                except:
                    # Ignore exceptions and keep the original cell value if unpacking fails
                    pass

                row.append(cellValue)

            data.append(row)

        # Convert the extracted columns and data into a dataset
        return system.dataset.toDataSet(columns, data)
    except Exception as e:
        # Handle any exceptions and return an empty dataset in case of errors
        return system.dataset.toDataSet([], [])
