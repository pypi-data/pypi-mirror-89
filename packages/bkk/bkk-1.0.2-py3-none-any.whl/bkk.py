###############################################################################################
#
# /$$$$$$$  /$$   /$$ /$$   /$$                                  /$$$$$$  /$$       /$$$$$$$ 
# | $$__  $$| $$  /$$/| $$  /$$/                                 /$$__  $$| $$      |_  $$_/
# | $$  \ $$| $$ /$$/ | $$ /$$/         /$$$$$$  /$$$$$$$       | $$  \__/| $$        | $$  
# | $$$$$$$ | $$$$$/  | $$$$$/         /$$__  $$| $$__  $$      | $$      | $$        | $$
# | $$__  $$| $$  $$  | $$  $$        | $$  \ $$| $$  \ $$      | $$      | $$        | $$
# | $$  \ $$| $$\  $$ | $$\  $$       | $$  | $$| $$  | $$      | $$    $$| $$        | $$
# | $$$$$$$/| $$ \  $$| $$ \  $$      |  $$$$$$/| $$  | $$      |  $$$$$$/| $$$$$$$$ /$$$$$$
# |_______/ |__/  \__/|__/  \__/       \______/ |__/  |__/       \______/ |________/|______/
#
###############################################################################################

import click
import requests
from datetime import datetime, timedelta
from scheduleItem import ScheduleItem
from config import *

def getRealTimeUrl(stopId, date):
	url="https://futar.bkk.hu/api/query/v1/ws/otp/api/where/schedule-for-stop.json"
	url += "?key=key&version=3&appVersion=version&includeReferences=true&stopId="
	url += stopId
	url += "&onlyDepartures=false&date="
	url += date
	return url

def getDateString(datetimeObj):
	return datetimeObj.strftime('%Y%m%d')


def getShortName_fromRouteId(data, routeId):
	"""Iterate through References to find the shortName of a given route"""
	for route in data["data"]["references"]["routes"]:
		if data["data"]["references"]["routes"][route]["id"] == routeId:
			shortName = data["data"]["references"]["routes"][route]["shortName"]
	
	return shortName		

def getListof_UpcomingScheduleItems(data, now):
	"""Selects schedule items inside the time window defined in config.py, returns them as a list"""
	ret = []

	schedules = data["data"]["entry"]["schedules"]

	for route in range(0, len(schedules)):

		for timePoint in schedules[route]["directions"][0]["stopTimes"]:

			fromNowOn = datetime.fromtimestamp(timePoint["arrivalTime"]) > now
			untilGivenMinutes = datetime.fromtimestamp(timePoint["arrivalTime"]) < now + timedelta(minutes=future_minutes)

			if fromNowOn and untilGivenMinutes: #inside the time window

				isRealTime = False
				"""
					The API only returns real-time data for a fraction of upcoming vehicles,
					so I need to select those, where predicted fields exist.
					If not, the flag is set false, and the static data is used. 
				"""
				try:
					if timePoint["predictedArrivalTime"] and timePoint["predictedDepartureTime"]:
						arrivalTime = datetime.fromtimestamp(timePoint["predictedArrivalTime"])
						departureTime = datetime.fromtimestamp(timePoint["predictedDepartureTime"])
						isRealTime = True

				except KeyError:
					arrivalTime = datetime.fromtimestamp(timePoint["arrivalTime"])
					departureTime = datetime.fromtimestamp(timePoint["departureTime"])
				

				shortName = getShortName_fromRouteId(data, schedules[route]["routeId"])
				newItem = ScheduleItem(shortName, arrivalTime, departureTime, isRealTime)
				ret.append(newItem)

	return ret

def sortKey(scheduleItem):
	return scheduleItem.arrivalTime

@click.command()
@click.option('--rt', is_flag=True , help='Display if data is real-time or from the static schedule')
def main(rt):
	"""Get the real-time struechedule of your favourite public transport stop in Budapest.

	Edit config.py to select stop, and set preferred time window."""

	now = datetime.now()

	url = getRealTimeUrl(STOPID, getDateString(now))
	r = requests.get(url)
	data = r.json()


	scheduleItems = getListof_UpcomingScheduleItems(data, now)

	"""
		The API returns schedule data only for the given day. If the time window defined in config.py
		overloops to the next day, the API has to be called again, to have results from after midnight.
	"""
	if getDateString(now + timedelta(minutes=future_minutes)) > getDateString(now): 
		url_tomorrow = getRealTimeUrl(STOPID, getDateString(now + timedelta(minutes=future_minutes)))
		r_tomorrow = requests.get(url_tomorrow)
		data_tomorrow = r_tomorrow.json()

		scheduleItems_tomorrow = getListof_UpcomingScheduleItems(data_tomorrow, now)
		scheduleItems.extend(scheduleItems_tomorrow) #append results from tomorrow to todays list

	
	"""
		Sorting elements by their arrivalTimes.
		By default, they're grouped by their routeIds.
	"""
	scheduleItems.sort(key=sortKey)

	print("\n current time: ", now.strftime('%X'))
	for  item in scheduleItems:
		arrival = item.arrivalTime.strftime('%X')
		departure = item.departureTime.strftime('%X')
		if rt:
			realtime = " (real-time)" if item.isRealTime else " (static)"
		else:
			realtime = ""
		print("    ", item.shortName, " arrives at: ", arrival, realtime)

if __name__ == '__main__':
	main()
