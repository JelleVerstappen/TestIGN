from ata.toast.util.cfg import Configs
from ata.toast.util.tasks import ToastTimeout, ToastClear
from ata.toast.util.toast import Toast, SessionMessenger

def toastNotification(message, timeout=None, sendTo='', **toastArgs):
	"""Send out toast notification and schedule the timeout
	
	Args:
		message: text to display in the toast message
		timeout: time in seconds that the message will appear before being removed
		sendTo: perspective session id to send to if left as blank will send to all sessions
		project: project to send the message to
		messageHandler: message handler to use from the SessionMessenger class
		backgroundColor: you can add backgroundColor to the args to change the background color of the toast, otherwise the style will be used. 
	Returns:
		None
	"""
	# Get the toast message & format session message args
	project=system.project.getProjectName()
	toast = Toast(message, **toastArgs)
	messengerArgs = SessionMessenger.args(project, Configs.ADD_MESSENGER, toast.props, sendTo)
	
	
	# Send toast message out to perspective sessions
	system.util.sendMessage(**messengerArgs)
	
	# Schedule toast timeout if timeout is > 0 (sends message to perspective sessions after the timeout period)
	if bool(timeout):
		task = ToastTimeout(toast.toastID, sendTo, project, Configs.TIMEOUT_MESSENGER)
		executeAfter = int(timeout*1000 + 250) # Added 0.25s additional delay to the timeout in case of latency or slower rendering
		Configs.getEngine().executeOnce(task, executeAfter)
	
	# Log notification	
	if Configs.ENABLE_LOGGING:
		Configs.getLogger().info('Toast Notification Added')
	return None
	
def toastClearOut(toastID, waitTime, project=system.project.getProjectName()):
	"""Creates a task that will clear out the toast notification from the Toast Handler if an animation is applied
		
	Args:
		toastID: id of the toast message to clear
		waitTime: time in seconds until the message is cleared from the handler
		project: project to send the message to
		messageHandler: message handler to use from the SessionMessenger class
	Returns:
		None
	"""
	# Create task instance and get the time to executeAfter
	task = ToastClear(toastID, project, Configs.CLEAROUT_MESSENGER)
	executeAfter = int(waitTime*1000) # Convert incoming waitTime to milliseconds
	
	# Schedule the task with the engine to execute later
	Configs.getEngine().executeOnce(task, executeAfter)
	return None