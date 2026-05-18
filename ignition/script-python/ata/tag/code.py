def readTags(tagPaths):
	return {tagPaths[x]: tagRead.value for x, tagRead in enumerate(system.tag.readBlocking(tagPaths))}

def readTag(tagPath):
	return system.tag.readBlocking([tagPath])[0].value

def getUDTName(tagPath):
	tagConfiguration = system.tag.getConfiguration(tagPath)[0]
	if str(tagConfiguration['tagType']) != 'UdtInstance':
		raise TypeError('Tag is not an UDT: {}'.format(tagPath))

	return tagConfiguration['typeId']

def writeTag(tagPath,value):
	return system.tag.writeBlocking([tagPath],[value])

def writeTags(tagPaths, values):
	return system.tag.writeBlocking(tagPaths, values)
