class ScheduleItem(object):
	"""class for stroring schedule data points, such as times, and routeIds"""
	def __init__(self, shortName, arrivalTime, departureTime, realTimeFlag):
		self.shortName = shortName
		self.arrivalTime = arrivalTime
		self.departureTime = departureTime
		self.isRealTime = realTimeFlag