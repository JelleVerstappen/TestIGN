class getLogger:
	def __init__(self, loggerName):
		"""
        Initializes a simple logger that can be used as a replacement for Ignitions system.util.getLogger(name) to print log message in the script console.
        
	    Args:
	        loggerName (str): The name of the logger.
        """
		self.logName = loggerName
	
	def printLog(self, prependStr, message):
#		print self.logName+prependStr+message+'\n'
		print self.logName+message+'\n'
	
	def tracef(self, message, *args):
		prependStr = " -- Trace:\n"
		fullMessage = message % (args)
		self.printLog(prependStr, fullMessage) 
	
	def debugf(self, message, *args):
		prependStr = " -- Debug:\n"
		fullMessage = message % (args)
		self.printLog(prependStr, fullMessage) 
	
	def infof(self, message, *args):
		prependStr = " -- Info:\n"
		fullMessage = message % (args)
		self.printLog(prependStr, fullMessage) 
	
	def warnf(self, message, *args):
		prependStr = " -- Warning:\n"
		fullMessage = message % (args)
		self.printLog(prependStr, fullMessage)  
	
	def errorf(self, message, *args):
		prependStr = " -- Error:\n"
		fullMessage = message % (args)
		self.printLog(prependStr, fullMessage) 
	
	def trace(self, message):
		prependStr = " -- Trace:\n"
		self.printLog(prependStr, message) 
	
	def debug(self, message):
		prependStr = " -- Debug:\n"
		self.printLog(prependStr, message) 
	
	def info(self, message):
		prependStr = " -- Info:\n"
		self.printLog(prependStr, message) 
	
	def warn(self, message):
		prependStr = " -- Warning:\n"
		self.printLog(prependStr, message)  
	
	def error(self, message):
		prependStr = " -- Error:\n"
		self.printLog(prependStr, message) 


def printDataset(dataset):
	"""
	Prints the contents of an Ignition dataset in a tabular format.
	
	Args:
	    dataset (Dataset): The Ignition dataset to be printed.
	Returns:
	    None
	"""
	rows = [dataset.getColumnNames()] + [list(r) for r in system.dataset.toPyDataSet(dataset)]
	columnsSize = [max([len(str(rows[y][x])) for y in range(len(rows))]) for x in range(dataset.getColumnCount())]
	for i, d in enumerate(rows):
		line = '|' + '|'.join([str(c).ljust(columnsSize[x] + 1) for x, c in enumerate(d)]) + '|'
		if i == 0: print('-' * len(line))
		print(line)
		if i == 0: print('|' + '-' * (len(line) - 2) + '|')
		if i == len(rows) - 1: print('-' * len(line))


def dirObject(obj, searchString = None):
	"""
	Displays information about an object.
	
	Args:
	    obj (object): The object to be inspected.
	    searchString (str, optional): If provided, filters and displays only members containing the specified string.
	
	Returns:
	    None
	"""
	print 'Type: '+str(type(obj))
	print 'Object: '
	pp.pprint(obj)
	print '' 
	members = dir(obj)
	for m in members:
		if searchString is None or searchString in m:
			print m