###
# Drew A. Clinkenbeard
# combat.py
# Used For Combat
# 3 - May - 2014
#
###

import time
import curses

import logger

class Combat():

	def __init__(self, p1,e1,window):
		"""
			combat takes a player object, an enemy object, and
			a window object. It renders the enemies in the window
			and a fight ensues.

		"""
		l = logger.Logger("combat.log")
		self.minX = minX	= 2
		#how far to the right we can go.
		#Leaving room for messages.
		self.maxX = maxX	= window.getmaxyx()[1] -3

		self.minY = minY	= 2
		##how far down we can go
		#leaving room for messages
		self.maxY = maxY	= window.getmaxyx()[0] -3

		self.pSide = self.minY,(self.maxX-10)
		self.eSide = self.minY,self.minX
		

		window.clear()
		window.border(0)


		keypresses = { 
						  
						# , 'quit':'q'
						  'a':['attack',self._attack]
						, 'd':['defend',self._defend]
						, 'i':['items',self._items]
						# , 'b':'bomb'
						, 'r':['run',self._run]
					}


		battle = True

		while battle:


			# enemy
			window.addstr(self.eSide[0],self.eSide[1],e1.icon.encode('utf-8'))
			window.addstr(self.eSide[0]+1,self.eSide[1],e1.etype.encode('utf-8'))

			# Player
			window.addstr(self.pSide[0],self.pSide[1],p1.icon.encode('utf-8'))
			window.addstr(self.pSide[0]+1,self.pSide[1],p1.name.encode('utf-8'))

			msg = "Keypresses.length == {0}".format(len(keypresses))
			l._log(msg)

			y = self.pSide[0]+4	
			for k in sorted(keypresses):
				ctrl = "{0} = {1}".format(k,keypresses[k][0])				
				window.addstr(y,self.pSide[1],ctrl.encode('utf-8'))
				y +=1
			
			line = "-"*self.maxX

			window.addstr(self.minY+3,self.minX,line)

			for z in range(self.minY+3,self.maxY):
				window.addstr(z,(self.maxX/2)-1,"|")

			self.__player(p1,window)
			self.__enemy(window)

			attack = u"\U0001F52A :{0}".format(p1.attack)
			window.addstr(self.pSide[0]+4,(self.maxX/2)+1,attack.encode("utf-8"), curses.A_NORMAL)
			# attack = u"Attack: {0}".format(p1.attack)
			# window.addstr(self.pSide[0]+4,(self.maxX/2)+3,attack.encode("utf-8"))

			window.refresh()

			key = window.getch()

			keypresses[key][1](p1,e1)

			# time.sleep(3)

			battle = False

	def __player(self,p1,window):
		pass
		# y = self.pSide[0]
		# x = self.pSide[1]
		# y = y + 4

		# attack = u"\U00002694 ".format(p1.attack)

		# window.addstr(y,x,attack.encode("utf-8"))
		# window.refresh()
		
	def __enemy(self, window):
		pass

	def _attack(self,p1,e1):
		pass

	def _defend(self,p1,e1):
		pass

	def _items(self,p1,e1):
		pass

	def _run(self,p1,e1):
		pass


