from uuid import uuid4

class SessionMessenger:
	"""Session Messenger class that is used to create the args for the toast messages etc"""
	
	@classmethod
	def args(cls, project, messageHandler, payload, sendTo):
		"""Creates the args to be used in the system.util.sendMessage function specifically for toasts"""
		return {
			'project': project
			, 'messageHandler': messageHandler
			, 'payload': payload
			, 'scope': 'CS'
			, 'clientSessionId': sendTo
		}

class Toast:
	"""Toast message class, contains the message and assigns an ID for this message
	
	Args:
		message: toast message
		kwargs: key word args for additional toast parameters you want to pass into the notification
	"""
	def __init__(self, message, **kwargs):
		self.message = message.strip()
		self.toastID = str(uuid4())
		self.instanceStyle = {}
		self.setProperties(**kwargs)
		
	def setProperties(self, **kwargs):
		"""Set the key word properties into the toast message"""
		for key, value in kwargs.items():
			setattr(self, key, value)
	
	@property
	def props(self):
		"""Creates a dict of the class variables"""
		return dict(self.__dict__)