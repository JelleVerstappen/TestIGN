import threading


### Get difference of two lists
### Checks what is in list 1 and not in list 2
### returns list of difference 
def listDiff(list1,list2):
	return list(set(list1) - set(list2))

### Get matches of two lists
### Checks what is in list 1 and in list 2
### returns list of matching values 
def listMatch(list1,list2):
	return list(set(list1) & set(list2))

def getLock(lockName='lock'):
	try:
		lock = system.util.getGlobals()[lockName]
	except:
		lock = threading.Lock()
		system.util.getGlobals()[lockName] = lock

	return lock

##### Split a string and return a row of the split dataset
def splitAndGet(string,separator,row): 
	dataset = string.split(separator)
	if abs(row) <= len(dataset):
		return dataset[row]
	else:
		return -1
		
##### Find needle in a haystack. 
def findNeedle(haystack, needle, n):
	start = haystack.find(needle)
	while start >= 0 and n > 1:
		start = haystack.find(needle, start+len(needle))
		n -= 1
	return start

##### Returns the max value of the dataset, only searches the fields in the search header list.
def findHigestValueInDataset(data,headersToSearch=[]):
	py_data = system.dataset.toPyDataSet(data)
	max_value = 0
	row_count = py_data.getRowCount()
	for i in range(row_count):
		for header in headersToSearch:
			value = py_data.getValueAt(i, header)
			if value > max_value:
				max_value = value
	return max_value 

##### Generates a random color
def randomColor():
	import random
	r = lambda: random.randint(0,255)
	color = ('#%02X%02X%02X' % (r(),r(),r()))
	return color
	

##### Creates a color variance
def getColorVariation(originalColor):
    import random

    # Remove the hashtag if present
    colorCode = originalColor.lstrip('#')

    decRange = 10
    darkenLighten = random.randint(-30, 30)

    rHex = colorCode[0:2]
    gHex = colorCode[2:4]
    bHex = colorCode[4:6]

    rDec = max(0, min(int(rHex, 16) + random.randint(-decRange, decRange) + darkenLighten, 255))
    gDec = max(0, min(int(gHex, 16) + random.randint(-decRange, decRange) + darkenLighten, 255))
    bDec = max(0, min(int(bHex, 16) + random.randint(-decRange, decRange) + darkenLighten, 255))

    newColor = "%02X%02X%02X" % (rDec, gDec, bDec)
    newColor = "#"+newColor if originalColor.startswith('#') else newColor

    return newColor

def getColorVariationThree(originalColor):
    import colorsys
    import random

    # Remove the hashtag if present
    colorCode = originalColor.lstrip('#')

    # Convert hex to RGB
    r, g, b = int(colorCode[0:2], 16), int(colorCode[2:4], 16), int(colorCode[4:6], 16)

    # Convert RGB to HSL (Hue, Saturation, Lightness)
    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

    # Adjust Hue (H)
    hueVariation = random.uniform(-30, 30)
    h = (h + hueVariation) % 360

    # Adjust Saturation (S) and Lightness (L) more intelligently
    saturationVariation = random.uniform(-0.1, 0.1)
    lightnessVariation = random.uniform(-0.1, 0.1)

    # Avoid extreme saturation and lightness values
    s = max(0, min(s + saturationVariation, 1))
    l = max(0.2, min(l + lightnessVariation, 0.8))

    # Convert HSL back to RGB
    r, g, b = [int(c * 255) for c in colorsys.hls_to_rgb(h, l, s)]

    newColor = "%02X%02X%02X" % (r, g, b)
    newColor = "#" + newColor if originalColor.startswith('#') else newColor

    return newColor
    
def uniqueList(list):
	unique = []
	for item in list:
		if item not in unique:
			unique.append(item)
	return unique
  
