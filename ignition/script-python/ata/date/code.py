def createDateTime(year, month, day, hour=0, minute=0, second=0):
    """
    Creates a DateTime object with the specified date and time components.

    Args:
        year (int): The year.
        month (int): The month (1-12).
        day (int): The day of the month.
        hour (int, optional): The hour (0-23). Defaults to 0.
        minute (int, optional): The minute (0-59). Defaults to 0.
        second (int, optional): The second (0-59). Defaults to 0.

    Returns:
        java.util.Date: The DateTime object.
    """
    return system.date.setTime(system.date.getDate(year, month - 1, day), hour, minute, second)


def getTime(inputDate):
    """
    Gets the hour, minute, and second components of a DateTime object.

    Args:
        inputDate (java.util.Date): The DateTime object.

    Returns:
        tuple: A tuple containing the hour, minute, and second.
    """
    hour = system.date.getHour24(inputDate)
    minute = system.date.getMinute(inputDate)
    second = system.date.getSecond(inputDate)
    return hour, minute, second


def fillDropdownWithYears(startYear):
    """
    Fills a dropdown dataset with years from startYear to the current year.

    Args:
        startYear (int): The starting year.

    Returns:
        com.inductiveautomation.ignition.common.Dataset: The dropdown dataset.
    """
    currentYear = system.date.getYear(system.date.now())
    headers = ["value", "label"]
    data = [[newYear, newYear] for newYear in range(startYear, currentYear + 1)]
    return system.dataset.toDataSet(headers, data)


def calculateMonth(year, month):
    """
    Calculates the start and end date of a month in the specified year.

    Args:
        year (int): The year.
        month (int): The month (1-12).

    Returns:
        list: A list containing [startDate, endDate].
    """
    startDate = system.date.getDate(year, month - 1, 1)
    endDate = system.date.getDate(year, month, 0)
    startDate = system.date.format(startDate, 'dd-MM-yyyy')
    endDate = system.date.format(endDate, 'dd-MM-yyyy')
    return [startDate, endDate]


def calculateQuarter(year, quarter):
    """
    Calculates the start and end date of a quarter in the given year.

    Args:
        year (int): The year.
        quarter (int): The quarter (1-4).

    Returns:
        list: A list containing [startDate, endDate].
    """
    startDate = system.date.getDate(year, quarter * 3 - 3, 1)
    endDate = system.date.getDate(year, quarter * 3, 0)
    startDate = system.date.format(startDate, 'dd-MM-yyyy')
    endDate = system.date.format(endDate, 'dd-MM-yyyy')
    return [startDate, endDate]


def secondsToTime(seconds, includeDays=False):
    """
    Converts a duration in seconds to a formatted time representation.

    Args:
        seconds (int or float): The duration in seconds.
        includeDays (bool, optional): Whether to include days in the formatted output. Default is False.

    Returns:
        dict: A dictionary containing the formatted time components.
            If includeDays is False: {"formatted": "HH:MM:SS", "hours": hours, "minutes": minutes, "seconds": seconds}
            If includeDays is True: {"formatted": "D days HH:MM:SS", "days": days, "hours": hours, "minutes": minutes, "seconds": seconds}
    """
    if type(seconds) == long:
    	seconds = int(seconds)
    
    if type(seconds) not in (int, float):
        raise TypeError("The given argument for seconds is of type '%s'. The function requires an argument of type 'int' or 'float.'" % (type(seconds).__name__))
	
    import math

    hours = int(math.floor(seconds / 3600))
    minutes = int(math.floor((seconds - (hours * 3600)) / 60))
    seconds = int(seconds - (hours * 3600) - (minutes * 60))

    if not includeDays:
        formatted = "%02d:%02d:%02d" % (hours, minutes, seconds)
        return {"formatted": formatted, "hours": hours, "minutes": minutes, "seconds": seconds}

    days = int(math.floor(hours / 24))
    hours = int(math.floor(hours % 24))
    dayStr = 'day' if days == 1 else 'days'

    formatted = "%d %s %02d:%02d:%02d" % (days, dayStr, hours, minutes, seconds)
    return {"formatted": formatted, "days": days, "hours": hours, "minutes": minutes, "seconds": seconds}


def recurringEvents(startDate, recurrenceDays = [False,False,False,False,False,False,False], endDate = 0, numberOfOccurrences = 0):
	"""
	Returns start and end date each time a recurring event takes can take place within a timespan or a set number of times.
	
	Args:
		startDate (datetime): start date
		recurrenceDays (list): list of booleans for a recurrence on each day. First value is sunday, last value is saturday. default([False,False,False,False,False,False,False])
		endDate (datetime): end date (default 0)
		numberOfOccurrences (int): number of occurences (default 0)
	returns:
		list: A list of all dates which comply to this recurrence
	"""
	startDates = []
	dayIndex = {1: recurrenceDays[0], 2: recurrenceDays[1], 3:recurrenceDays[2], 4: recurrenceDays[3], 5: recurrenceDays[4], 6: recurrenceDays[5], 7: recurrenceDays[6]}
	
#	# Calculate based on number of occurences
	if numberOfOccurrences != 0:
		for i in range(7*numberOfOccurrences):
			day = system.date.addDays(startDate, i)
			dayNr = system.date.getDayOfWeek(day)
			if dayIndex[dayNr] == True:
				startDates.append(day)
	
#	# Calculate based on enddate
	else:
		daysBetween = system.date.daysBetween(startDate, endDate)
		for i in range(daysBetween + 1):
			day = system.date.addDays(startDate, i)
			dayNr = system.date.getDayOfWeek(day)
			if dayIndex[dayNr] == True:
				startDates.append(day)
	return startDates