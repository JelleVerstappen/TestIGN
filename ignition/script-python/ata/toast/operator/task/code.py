from abc import ABCMeta, abstractmethod
from java.lang import Runnable

# Docs: https://docs.oracle.com/javase/8/docs/api/java/lang/Runnable.html
class AbstractTask(Runnable):
	__metaclass__ = ABCMeta
	"""Basic Execution Engine Task
	
	Args:
		name: name given to this task, used as the logger name
		taskLogging: log information for this task
		logEnabled: boolean flag to enable logging in the run function
	"""
	def __init__(self, name, logMessage, logEnabled):
		self.name = name
		self.logMessage = logMessage
		self.logEnabled = logEnabled
	
	@abstractmethod
	def action(self):
		"""Task action to be executed in the engine"""
		pass
		
	@property
	def loggerName(self):
		"""Get the name of the logger for this task"""
		return self.name.replace(' ', '-')
		
	def log(self):
		"""Task logging function"""
		logger = system.util.getLogger(self.loggerName)
		logger.info(str(self.logMessage))
		return None
		
	def run(self):
		"""Runnable run method runs class action/log method"""
		self.action()
		if self.logEnabled:
			self.log()
		return None
		