from items import *
from math import floor, sqrt,ceil

class Player():

	def __init__(self, name="Samalander",score=0, race='human',xp=1, debug=False):
		
		self.xp 		= 0
		self.level 		= 0
		self.attack 	= 0
		self.defense 	= 0
		self.__setLevel(xp)

		self.__setMaxHP()
		self.health = self.maxHealth
		self.score  = score
		self.inventory = items.getItems()
		for item in self.inventory:
			self.inventory[item]['quantity'] = 0
		self.carryLimit = 500
		self.currentCarry = 0
		self.name = name
		

		self.icon = u"\U0001f355"

		# Player Class stuff.
		# Most of this is not implemented
		# Sight radius This will later be a factor of player class
		self.sight=3
		self.attack  = 5
		self.defense = 5

		self.__setAttack()
		self.__setDefense()

	def __repr__(self):
		out  = "Final Health : {0}\n".format(self.health)
		out += "Final Score  : {0}\n".format(self.score)
		out += "Ending Level : {0}\n".format(self.level)


	def setName(self,name):
		self.name = name

	def getName(self):
		return self.name
	
	def __setLevel(self,exp):
		self.level = int(floor(sqrt(self.xp)))
		return self.level

	def __setMaxHP(self):
		self.maxHealth = int(ceil((self.level*10)))

	def __setHealth(self,health):
		self.health = health

	def __addHealth(self,health):
		self.health += health

	def getInventory(self):
		return self.inventory

	def checkInventory(self,item):
		return item in inventory

	def __setScore(self, score):
		self.score = score
		return self.score

	def addScore(self,score):
		self.score += score
		return self.score

	def getScore(self):
		return self.score

	def setLevel(self):
		self.level = int(floor(sqrt(self.xp)))

	def __setAttack(self):
		self.attack = self.attack + int(floor(sqrt(self.xp)))

	def __setDefense(self):
		self.defense = self.defense + int(ceil(sqrt(self.xp))) + floor(self.maxHealth/2)

	def setExp(self,exp):
		self.exp = exp

	def addXP(self, xp):
		self.xp += xp
		if (floor(sqrt(self.xp)) > self.level):
			self.levelUp()
			
	def levelUp(self):
		self.__setLevel()
		self.__setMaxHP()
		self.__setAttack()
		self.__setDefense()

	def addItem(self,item,itemNum):

		# if item not in items.getItems():
		# 	return False

		if item not in self.inventory:
			# self.inventory[item] = {
			# 	'quantity':itemNum
			# }
			return False
		elif self.inventory[item]['quantity'] >=  self.inventory[item]['max']:
			return False
		elif (self.inventory[item]['quantity']) + itemNum >= self.inventory[item]['max']:
			# added = ((self.inventory[item]['max']+itemNum)-self.inventory[item]['quantity']))
			# if self.currentCarry + (added * self.inventory[item]['weight']) > self.carryLimit:
			# 	return False
			self.inventory[item]['quantity'] = self.inventory[item]['max']
			self.addScore(self.inventory[item]['score'])
			return True
		else:
			self.inventory[item]['quantity'] += itemNum
			return True



