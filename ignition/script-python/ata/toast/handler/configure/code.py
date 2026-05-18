### Toast handler configuration functions for toast location, animation,###
from ata.toast.util.handler_configuration import Locations, Animations

def getLocation(location):
	"""Gets the coordinates to the set the Toast Handler to set the message at
	
	Args:
		location: string of the location value (top-left, top-right, center, bottom-left, bottom-right)
	Returns:
		pyDict of the coordinates if location is invalid defaults to bottom-right
	"""
	return Locations.getCoordinates(location)
	
def getAnimation(animation):
	"""Gets the css animation to apply to the toast message
	
	Args:
		animation: name of the animation to get
	Returns:
		css animation string to apply to the toast message
	"""
	return Animations.getAnimation(animation)