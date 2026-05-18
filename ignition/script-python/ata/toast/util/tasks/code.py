from ata.toast.util.cfg import Configs
from ata.toast.util.toast import SessionMessenger
from ata.toast.operator.task import AbstractTask

class ToastTimeout(AbstractTask):
	"""Task for timing out a toast notification
	
	Args:
		toastID: id of the toast message that will timeout goes into the payload
		sendTo: perspective session id to send to if left as blank will send to all sessions
		project: project to send the message to
		messageHandler: message handler to use from the SessionMessenger class
	"""
	def __init__(self, toastID, sendTo, project, messageHandler):
		self.args = SessionMessenger.args(project, messageHandler, {'toastID': toastID}, sendTo)
		AbstractTask.__init__(self, name=Configs.LOGGER_NAME, logMessage='Toast Notification Timeout', logEnabled=Configs.ENABLE_LOGGING)
		
	def action(self):
		"""Send the message to timeout the toast notification, called by the execution engine"""
		system.util.sendMessage(**self.args)
		return None
		
class ToastClear(AbstractTask):
	"""Task for clearing a toast message once the animation is complete
	
	Args:
		toastID: id of the toast message that will timeout goes into the payload
		sendTo: perspective session id to send to if left as blank will send to all sessions
		project: project to send the message to
		messageHandler: message handler to use from the SessionMessenger class
	"""
	def __init__(self, toastID, project, messageHandler):
		self.args = SessionMessenger.args(project, messageHandler, {'toastID': toastID}, '')
		AbstractTask.__init__(self, name=Configs.LOGGER_NAME, logMessage='Toast Notification Cleared', logEnabled=Configs.ENABLE_LOGGING)
		
	def action(self):
		"""Send the message to timeout the toast notification, called by the execution engine"""
		system.util.sendMessage(**self.args)
		return None