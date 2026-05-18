### These functions are called from message session events, sends perspective messages to the toast handler component ###
def addToast(toast):
	"""Called from perspective message session event (acts as a relay between the gateway message to the component), goes to the Toast Handler
	
	Args:
		toast: ToastMessage class dictionary, contains the message and toastID
	Returns:
		None
	"""
	system.perspective.sendMessage('toast-add', toast, scope='session')
	return None
	
def closeToast(toastID):
	"""Called from perspective message session event or message close button, goes to the Toast Handler -- closes the toast from the handler
		
	Args:
		toastID: id of the toast message to close out
	Returns:
		None
	"""
	system.perspective.sendMessage('toast-close', {'toastID': toastID}, scope='session')
	return None
	
def clearToast(toastID):
	"""Called from perspective message session event or message close button, goes to the Toast Handler -- clears the toast from the handler instances
		
	Args:
		toastID: id of the toast message to close out
	Returns:
		None
	"""
	system.perspective.sendMessage('toast-clear', {'toastID': toastID}, scope='session')
	return None