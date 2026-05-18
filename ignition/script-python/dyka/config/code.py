tagProvider = 'NLSTWDYK'

def assetPath(asset):
	"""
	Returns asset path based on asset code.
	
	Args:
		asset (str): The name of the asset or machine to navigate to.
		
	
	Returns:
		str: The cell group and cell of the corresponding asset.
	"""
	path = ""
	assetMappingDict = {
					"SIL":{"CellGroup":"MAT", "Cell":"MST"},
					"RAW":{"CellGroup":"MAT", "Cell":"MHL"},
					"MEXT":{"CellGroup":None, "Cell":"EXT"},
					"CEXT01":{"CellGroup":None, "Cell":"EXT"},
					"CEXT02":{"CellGroup":None, "Cell":"EXT"},
					"VAC":{"CellGroup":None, "Cell":"FOR"},
					"COO":{"CellGroup":None, "Cell":"FOR"},
					"WTS":{"CellGroup":None, "Cell":"FOR"},
					"PRN":{"CellGroup":None, "Cell":"PRN"},
					"HAUL":{"CellGroup":None, "Cell":"HAUL"},
					"CUT":{"CellGroup":None, "Cell":"CUT"},
					"BEL":{"CellGroup":None, "Cell":"BEL"},
					"STC":{"CellGroup":None, "Cell":"STC"}
	}
	
	try:
		path += assetMappingDict[asset]["CellGroup"] + "/" if assetMappingDict[asset]["CellGroup"] is not None else ""
		path += assetMappingDict[asset]["Cell"] + "/" if assetMappingDict[asset]["Cell"] is not None else ""
		path += asset
	except:
		pass
	
	return path

def navigate(to, line = None):
	"""
	Returns the correct URL within the Ignition project
	based on the provided asset name.
	
	Args:
		to (str): The name of the asset or machine to navigate to.
		line (str): The line name to navigate to
		
	
	Returns:
		str: The URL path of the corresponding page in the ControlRoom project.
	"""
	
	url = '/'
	urlMappingDict = {
					'CuttingUnit': '/ControlRoom/Assets/CuttingUnit/CuttingUnit/%s' % line,
					'Extruder': '/ControlRoom/Assets/Extruder/Overview/Extruder/%s' % line,
					'Printer': '/ControlRoom/Assets/Printer/Overview/Printer/%s' % line,
					'HaulOff': '/ControlRoom/Assets/HaulOff/Overview/HaulOff/%s' % line,
					'RawMaterialTransport': '/ControlRoom/Assets/RawMaterialTransport/Overview/RawMaterialTransport/%s' % line,
					'Silo': '/ControlRoom/Assets/Silo/Overview/Silo/%s' % line,
					'VacuumAndCooling': '/ControlRoom/Assets/VacuumAndCooling/Overview/VacuumAndCooling/%s' % line,
					'FormingMachine': '/Trompbank',
					'PipeThicknessScanner': '/Wanddiktescanner',
					'PipeStacker': '/Aflegger',
					'Quality': '/ControlRoom/Quality/Quality/%s' % line
	}
	
	try:
		url = urlMappingDict[to]
	except:
		url = '/'
	return url