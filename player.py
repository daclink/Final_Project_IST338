###
# Drew A. Clinkenbeard
# player.py
# used to create the player objects
# 29 - April - 2014
#
###
from items import *
from math import floor, sqrt, ceil

class Player():

	def __init__(self, name="Samalander",score=0, char_class='human',xp=10, debug=False):
		"""
			create a player character. Initializes health, xp, score,char_class, name, and debug

			inputs:	str name: the player name. Default Samalander (it's from a book)
					int score: the player score. Defualt 0
					str char_class:	The player character class. This will be used for stuff later default: human
					int xp:	the players experience points. Currently not used. Default: 0
					bool debug: Used for logging messages and such. Default False

			output: Returns a player character 

		"""
		self.char_class = char_class
		self.xp 		= 0
		self.level 		= 0
		self.attack 	= 0
		self.defense 	= 0
		self.__setLevel()

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
		"""
			used to set the name... I am using a setter because I might want to
			check available names later.

			inputs: str name: the player name

			output: none but it modifies self.name
		"""
		self.name = name

	def getName(self):
		"""
			returns the players name. 
			Probably not necessary.
		"""
		return self.name
	
	def __setLevel(self):
		"""
			Used to set the players level.
			inputs: none

			outputs: none but it modifies self.level
		"""
		self.level = int(floor(sqrt(self.xp)))
		return self.level

	def __setMaxHP(self):
		"""
			determines player health based on level.
			When different character classes, and more stats, are added
			this will change

			Inputs:	none

			Outputs: none but it modifies self.maxHealth
		"""
		self.maxHealth = int(ceil((self.level*10)))

	def __setHealth(self,health):
		"""
			used to set self.health

			inputs: int health

			output: none but it modifies self.health
		"""
		self.health = health

	def __addHealth(self,health):
		"""
			used to adjust self.health

			inputs: int health

			output: none but it modifies self.health
		"""
		self.health += health

	def getInventory(self):
		"""
			get the current player inventory.

			Inputs: none

			Ouput: returns self.inventory
		"""
		return self.inventory

	def checkInventory(self,item):
		"""
			Do I have that item?
			inputs:	str item 

			output boolean
		"""
		return item in inventory

	def __setScore(self, score):
		"""
			used to set self.score

			inputs: int score

			output: none but it modifies self.score
		"""
		self.score = score
		return self.score

	def addScore(self,score):
		"""
			used to adjust self.score

			inputs: int score

			output: none but it modifies self.score
		"""
		self.score += score
		return self.score

	def getScore(self):
		"""
			Returns self.score

			inputs: none

			output: returns self.score
		"""
		return self.score

	def setLevel(self):
		"""
			used to set self.level

			inputs: None based off of self.xp

			output: none but it modifies self.level
		"""
		self.level = int(floor(sqrt(self.xp)))

	def __setAttack(self):
		"""
			generate the players base attack level

			no inputs or outputs makes use of self.xp and self.attack
		"""
		self.attack = self.attack + int(floor(sqrt(self.xp)))

	def __setDefense(self):
		"""
			set the base self.defense

			no inputs or outputs but makes use of self.xp and self.attack. This will also
			make use of different racial characteristics when those are implemented
		"""
		self.defense = self.defense + int(ceil(sqrt(self.xp))) + floor(self.maxHealth/2)

	def setXp(self,xp):
		"""
			used to set self.xp

			inputs: int xp

			output: none but it modifies self.xp
		"""
		self.xp = xp

	def addXP(self, xp):
		"""
			used to adjust self.xp

			inputs: int xp

			output: none but it modifies self.xp
		"""
		self.xp += xp
		if (floor(sqrt(self.xp)) > self.level):
			self.levelUp()
			
	def levelUp(self):
		"""
			DING!
			When an xp goal is reached these processes update everything associated with that.
			no inputs or outputs but it calls a bunch of stuff
		"""
		self.__setLevel()
		self.__setMaxHP()
		self.__setAttack()
		self.__setDefense()

	def addItem(self,item,quantity):
		"""
			Add an item to the inventory.
			Currently this doesn't allow the addition of any item that isn't in the
			Items class.
			I will likely create an equipment class later on that will add functionality

			inputs: str item the item to check for 
					quantity: the quantity of the item to add.
		"""

		# if item not in items.getItems():
		# 	return False

		if item not in self.inventory:
			# self.inventory[item] = {
			# 	'quantity':quantity
			# }
			return False
		elif self.inventory[item]['quantity'] >=  self.inventory[item]['max']:
			return False
		elif (self.inventory[item]['quantity']) + quantity >= self.inventory[item]['max']:
			# added = ((self.inventory[item]['max']+quantity)-self.inventory[item]['quantity']))
			# if self.currentCarry + (added * self.inventory[item]['weight']) > self.carryLimit:
			# 	return False
			self.inventory[item]['quantity'] = self.inventory[item]['max']
			self.addScore(self.inventory[item]['score'])
			return True
		else:
			self.inventory[item]['quantity'] += quantity
			return True



