def doPost(request, session):
	data = request['postData']
	values = data['values']
	currentTime = system.date.now()
	formatString = "Ignition responded at {}".format(currentTime)
	return {'html': formatString}