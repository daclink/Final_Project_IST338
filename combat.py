###
# Drew A. Clinkenbeard
# combat.py
# Used For Combat
# 3 - May - 2014
#
###

import time;

class Combat():

	def __init__(self, p1,e1,window):
		"""
			combat takes a player object, an enemy object, and
			a window object. It renders the enemies in the window
			and a fight ensues.

		"""

		self.minX = minX	= 0
		#how far to the right we can go.
		#Leaving room for messages.
		self.maxX = maxX	= window.getmaxyx()[1]

		self.minY = minY	= 0
		##how far down we can go
		#leaving room for messages
		self.maxY = maxY	= window.getmaxyx()[0] - 5
		window.clear()
		window.border(0)
		window.addstr(2,2,"HI!")
		
		window.refresh()

		time.sleep(1)

