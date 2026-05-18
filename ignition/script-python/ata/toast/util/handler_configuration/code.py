from ata.toast.util.util import BasicContainer

class Locations(BasicContainer):
	"""Toast Notification location class, contains the css style variables for setting the toast handler location"""
	CONTENT = {
		'top-left': {
			'coordinates': {'overflow': 'visible', 'position': 'absolute', 'top': 5, 'left': 5, 'zIndex': -1}
		}
		, 'top-right': {
			'coordinates': {'overflow': 'visible', 'position': 'absolute', 'top': 5, 'right': 5, 'zIndex': -1}
		}
		, 'center': {
			'coordinates': {'overflow': 'visible', 'position': 'absolute', 'top': 5, 'left': 5, 'bottom': 5, 'right': 5, 'zIndex': -1}
		}
		, 'bottom-left': {
			'coordinates': {'overflow': 'visible', 'position': 'absolute', 'bottom': 5, 'left': 5, 'zIndex': -1}
		}
		, 'bottom-right': {
			'coordinates': {'overflow': 'visible', 'position': 'absolute', 'bottom': 5, 'right': 5, 'zIndex': -1}
		}
	}
	@classmethod
	def getCoordinates(cls, location):
		"""Get the coordinates for the input location"""
		return cls.getFeature(location, 'coordinates')

class Animations(BasicContainer):
	""" """ 
	CONTENT = {
		'enter-right': {
			'enter': {'animation-name': 'slide-in-right-enter', 'animation-duration': '2s', 'animation-timing-function': 'linear'
				, 'animation-direction': 'normal', 'animation-fill-mode': 'forwards', 'animation-play-state': 'running'}
			, 'exit': {'animation-name': 'slide-in-right-exit', 'animation-duration': '2s', 'animation-timing-function': 'linear'
				, 'animation-direction': 'normal', 'animation-fill-mode': 'forwards', 'animation-play-state': 'running'}
		}
		, 'enter-left': {
			'enter': {'animation-name': 'slide-in-left-enter', 'animation-duration': '2s', 'animation-timing-function': 'linear'
				, 'animation-direction': 'normal', 'animation-fill-mode': 'forwards', 'animation-play-state': 'running'}
			, 'exit': {'animation-name': 'slide-in-left-exit', 'animation-duration': '2s', 'animation-timing-function': 'linear'
				, 'animation-direction': 'normal', 'animation-fill-mode': 'forwards', 'animation-play-state': 'running'}
		}
		, 'enter-top': {
			'enter': {'animation-name': 'slide-in-top-enter', 'animation-duration': '2s', 'animation-timing-function': 'linear'
				, 'animation-direction': 'normal', 'animation-fill-mode': 'forwards', 'animation-play-state': 'running'}
			, 'exit': {'animation-name': 'slide-in-top-exit', 'animation-duration': '2s', 'animation-timing-function': 'linear'
				, 'animation-direction': 'normal', 'animation-fill-mode': 'forwards', 'animation-play-state': 'running'}
		}
		, 'enter-bottom': {
			'enter': {'animation-name': 'slide-in-bottom-enter', 'animation-duration': '2s', 'animation-timing-function': 'linear'
				, 'animation-direction': 'normal', 'animation-fill-mode': 'forwards', 'animation-play-state': 'running'}
			, 'exit': {'animation-name': 'slide-in-bottom-exit', 'animation-duration': '2s', 'animation-timing-function': 'linear'
				, 'animation-direction': 'normal', 'animation-fill-mode': 'forwards', 'animation-play-state': 'running'}
		}
		, 'fade-in-out': {
			'enter': {'animation-name': 'fade-in', 'animation-duration': '2s', 'animation-timing-function': 'linear'
				, 'animation-direction': 'normal', 'animation-fill-mode': 'forwards', 'animation-play-state': 'running'}
			, 'exit': {'animation-name': 'fade-out', 'animation-duration': '2s', 'animation-timing-function': 'linear'
				, 'animation-direction': 'normal', 'animation-fill-mode': 'forwards', 'animation-play-state': 'running'}
			}
	}
	
	@classmethod
	def getAnimation(cls, animation):
		""" """
		return cls.getItem(animation)