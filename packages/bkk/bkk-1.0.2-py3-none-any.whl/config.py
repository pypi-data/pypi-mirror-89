"""
	STOPID: defines stop to watch. 
	Search STOPIDs on futar.bkk.hu: hover over stop, STOPID is in the header, right under the name of the stop.
	Remove the # from the beginning of the Id, and add BKK_ to it.

	Example stop: Szent Gellért tér, Tram stop to Pest. 
	Id on futar.bkk.hu: #008591 so the STOPID has to be BKK_008591

"""

STOPID = "BKK_008591" #Szent Gellért tér, Tram stop to Pest


"""
	This value defines the time window, in which the program displays the schedule items. 
"""
future_minutes = 60