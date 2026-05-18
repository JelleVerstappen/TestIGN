### From LIB
def addPassword(username, password):
	# Add pasword to password table
#	try:
	if len( system.db.runPrepQuery(''' SELECT username FROM ignition_users WHERE username = ? ''', [username], ata.config.userDB) ) == 0:
		system.db.runPrepUpdate('''INSERT INTO ignition_users VALUES(? , ?, Null, Null, Null)''', [ username, password ], ata.config.userDB)
	else:
		system.db.runPrepUpdate('''UPDATE ignition_users SET password = ? WHERE username = ?''', [ password, username ], ata.config.userDB)
#	except:
#		pass

def updatePicture(username, bytes):
	# If there is no record in DB yesy so create it
	if len( system.db.runPrepQuery('''SELECT username FROM ignition_users WHERE username = ? ''', [username], ata.config.userDB) ) == 0:
		system.db.runPrepUpdate('''INSERT INTO ignition_users VALUES(? , Null, Null, Null, ?)''', [username, bytes], ata.config.userDB)
	else:
		system.db.runPrepUpdate('''UPDATE ignition_users SET image = ? WHERE username = ? ''', [bytes, username], ata.config.userDB)		


def deleteUser(username):

	if len( system.db.runPrepQuery('''SELECT username FROM ignition_users WHERE username = ? ''', [username], ata.config.userDB) ) != 0:
		system.db.runPrepUpdate('''DELETE FROM ignition_users WHERE username = ?''', [username], ata.config.userDB)