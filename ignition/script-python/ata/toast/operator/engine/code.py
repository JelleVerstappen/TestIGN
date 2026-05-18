from com.inductiveautomation.ignition.common.execution.impl import BasicExecutionEngine

# Docs: https://files.inductiveautomation.com/sdk/javadoc/ignition79/793/com/inductiveautomation/ignition/common/execution/impl/BasicExecutionEngine.html#schedule-java.lang.String-java.lang.Runnable-java.lang.String-
class Engine(BasicExecutionEngine, object):
	GLOBAL_KEY = 'basic-execution-engine'
	def __new__(cls, engineName):
		""" """
		cls.setGlobalKey()
		if cls.isRunning(engineName):
			print 'Engine is running.'
			engine = cls.getEngine(engineName)
		else:
			print 'New engine created.'
			engine = super(Engine, cls).__new__(cls)
		return engine
		
	def __init__(self, engineName):
		self.engineName = engineName
		self.setEngine()
	
	### Instance Methods ###
	def setEngine(self):
		"""Set the engine into the globals"""
		system.util.getGlobals()[self.GLOBAL_KEY].update({self.engineName: self})
	
	### Class Methods ###
	@classmethod
	def isRunning(cls, engineName):
		"""Check if the engine if available"""
		return engineName in cls.getEngines().keys()
		
	@classmethod
	def getEngines(cls):
		"""Get the engines dict from the globals, returns empty dict if globalKey does not exists"""
		return system.util.getGlobals().get(cls.GLOBAL_KEY, {})
		
	@classmethod
	def getEngine(cls, engineName):
		"""Get the engine from the globals returns none if no matching name"""
		return cls.getEngines().get(engineName)
		
	@classmethod
	def deleteEngine(cls, engineName):
		"""Shutdown the execution engine and remove from the globals"""
		if cls.isRunning(engineName):
			cls.shutdownEngine(engineName)
			del system.util.getGlobals()[cls.GLOBAL_KEY][engineName]
		else:
			pass
		return None
		
	@classmethod
	def shutdownEngine(cls, engineName):
		"""Shutdown the specified execution engine to stop all further tasks"""
		if cls.isRunning(engineName):
			engine = cls.getEngine(engineName)
			engine.shutdown()
		else:
			pass
		return None
		
	@classmethod
	def setGlobalKey(cls):
		"""Set the global key into globals"""
		if not cls.getEngines():
			system.util.getGlobals()[cls.GLOBAL_KEY] = {}
		return None