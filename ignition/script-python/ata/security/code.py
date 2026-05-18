def writePermission(url, currentRole):
	if url == '/':
		# If the designer is used always return true
		return True
	data = system.tag.readBlocking("[default]Navigation/Navigation data")[0].value
	data = system.dataset.toPyDataSet(data)
	writeCol = data.getColumnIndex("required_write_roles")
	readCol = data.getColumnIndex("required_roles")
	pathCol = data.getColumnIndex("navigation_path")
	currentRoleList = []
	writeUsers = ''
	
	# Get the roles from the user
	for role in currentRole:
		currentRoleList.append(role)
		
	# Find the row in the data that matches the url and get the read roles from it
	for navRole in range(data.getRowCount()):
		if data.getValueAt(navRole,pathCol) == url: 
			readUsers = data.getValueAt(navRole,readCol)
	
	# Check if the roles matches the read rights of the page, otherwise send user to a blank page
	readUsersList = readUsers.split(',')
	readAllowed = ata.function.listMatch(readUsersList, currentRoleList)
	if not readAllowed:
		system.perspective.navigate('/')
		return 
	
	# Find the row in the data that matches the url and get the write roles from it
	for navRole in range(data.getRowCount()):
		if data.getValueAt(navRole,pathCol) == url: 
			writeUsers = data.getValueAt(navRole,writeCol)
	
	# Check if the user is allowed to write, if yes return true else false.		
	writeUsersList = writeUsers.split(',')
	writeAllowed = ata.function.listMatch(writeUsersList, currentRoleList)
	if writeAllowed: 
		return True
	else:
		return False