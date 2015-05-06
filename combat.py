###
# Drew A. Clinkenbeard
# combat.py
# Used For Combat
# 3 - May - 2014
#
###

import time
import curses
import random

import logger

class Combat():

	def __init__(self, p1,e1,window):
		"""
			combat takes a player object, an enemy object, and
			a window object. It renders the enemies in the window
			and a fight ensues.

		"""
		self.l = logger.Logger("combat.log")
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

		p1.pSide = self.pSide
		

		window.clear()
		window.border(0)


		keypresses = { 
						  
						# , 'quit':'q'
						  'a':'attack'
						, 'd':'defend'
						, 'i':'items'
						# , 'b':'bomb'
						, 'r':'run'
					}


		battle = True
		# l._log("p1\n{0}".format(p1))
		while battle:

			# enemy
			window.addstr(self.eSide[0],self.eSide[1],e1.icon.encode('utf-8'))
			window.addstr(self.eSide[0]+1,self.eSide[1],e1.etype.encode('utf-8'))
			health = "{0}/{1}".format(e1.hp,e1.maxHP)
			window.addstr(self.eSide[0]+2,self.eSide[1],health.encode('utf-8'))

			# Player
			window.addstr(self.pSide[0],self.pSide[1],p1.icon.encode('utf-8'))
			window.addstr(self.pSide[0]+1,self.pSide[1],p1.name.encode('utf-8'))
			health = "{0}/{1}".format(p1.health,p1.maxHealth)
			window.addstr(self.pSide[0]+2,self.pSide[1],health.encode('utf-8'))

			# msg = "Keypresses.length == {0}".format(len(keypresses))
			# l._log(msg)

			# show keys
			y = self.pSide[0]+4	
			for k in sorted(keypresses):
				ctrl = "{0} = {1}".format(k,keypresses[k])				
				window.addstr(y,self.pSide[1],ctrl.encode('utf-8'))
				y +=1
			
			line = "-"*self.maxX

			window.addstr(self.minY+3,self.minX,line)

			# add a dividing line
			for z in range(self.minY+3,self.maxY):
				window.addstr(z,(self.maxX/2)-1,"|")

			self.__player(p1,window)
			self.__enemy(window)

			attack = u"\U0001F52A :{0}".format(p1.attack)
			window.addstr(self.pSide[0]+4,(self.maxX/2)+1,attack.encode("utf-8"), curses.A_NORMAL)
			# attack = u"Attack: {0}".format(p1.attack)
			# window.addstr(self.pSide[0]+4,(self.maxX/2)+3,attack.encode("utf-8"))


			window.refresh()

			# Get key press and parse it
			key = chr(window.getch())
			msg = "Key pressed = {0}".format(key)
			# l._log(msg)
			if key in keypresses:
				self._parser(key,p1,e1,window)
			else:
				battle = False

			window.clear()

			# time.sleep(3)

			# battle = False

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

	def _parser(self,key,p1,e1,window):
		"""
			used to parse the key the player input.
		"""
		if key == 'a':
			damage = self._attack(p1,e1)
			try:
				e1.damage(damage)
			except Exception as e:
				self.l._err(e,damage )
			msg = "{0} hit {1} for {2}".format(p1.name,e1.etype,damage)
			window.addstr(1,1,msg)
			window.refresh()
			time.sleep(1)
			

		elif key == 'd':
			damage = self._defend(p1,e1)
			
		elif key == 'i':
			self._items(p1)
		elif key == 'r':
			self._run(p1)

	
	def _attack(self,attacker,defender):
		"""
			Calculate the hit
			For now this is a pretty simple calculation.
			inputs: attacker either a player or enemy object
					defender either a player or enemy object

			output: int damage the amount of damage done

		"""
		self.critical = False
		roll = self.dX()

		if roll >=19:
			damage = attacker.attack*2
		elif roll >=2:
			damage = attacker.attack - (random.choice(range(0,defender.defense+1)))
		else:
			damage = 0 

	

		return damage

	def _defend(self,p1,e1):
		pass

	def _items(self,p1):
		pass

	def _run(self,p1,e1):
		pass

	@staticmethod
	def dX(sides=20):
		"""
			return a die roll.
			inputs: int sides, the number of sides the die should have
			output:	int between 1 and sides (+1 to include all sides)
		"""
		return random.choice(range(1,sides+1))


