from ata.toast.operator.engine import Engine

### Toast Notification Configs ###
class Configs:
	ENGINE_NAME = 'toast-engine' # Name of the engine executing toast notification tasks
	LOGGER_NAME = 'TOAST-MESSAGE' # Name of the logger for the toast messages
	ENABLE_LOGGING = True # Boolean flag to enable logging for toast notifications that are add and timed out
	
	# Perspective session event message handlers
	ADD_MESSENGER = 'toast-notification' # Adds toast notifcation to project
	TIMEOUT_MESSENGER = 'toast-timeout' # Removes a toast on timeout
	CLEAROUT_MESSENGER = 'toast-clearout' # Clears the handler of the message

	### Config Functions ###
	@classmethod
	def getEngine(cls):
		"""Get the execution engine based on ENGINE_NAME script property"""
		return Engine(cls.ENGINE_NAME)
	
	@classmethod
	def getLogger(cls):
		"""Get the logger for the toast notifications"""
		return system.util.getLogger(cls.LOGGER_NAME)
