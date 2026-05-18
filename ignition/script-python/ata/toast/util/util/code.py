class BasicContainer:
	"""Generic container class, used for setting the handler location/animation"""
	CONTENT = {}
	@classmethod
	def isValid(cls, item):
		"""Boolean check if item is in the CONTENT property"""
		return item in cls.CONTENT.keys()
		
	@classmethod
	def getAvailable(cls):
		"""Get the pyDict of the available content"""
		return cls.CONTENT.copy()
		
	@classmethod
	def getItem(cls, item):
		"""Get the pyDict of the input location"""
		return cls.CONTENT.get(item, {}).copy()
		
	@classmethod
	def getFeature(cls, item, feature):
		"""Get the coordinates for the input location"""
		_item = cls.getItem(item)
		return _item.get(feature, {}).copy()