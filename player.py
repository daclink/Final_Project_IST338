from items import *

class Player():

	def __init__(self, name="Samalander",maxHealth=100,score=0, race='human',  level=1, debug=False):
		self.maxHealth = maxHealth
		self.health = self.maxHealth
		self.score  = score
		self.inventory = items.getItems()
		for item in self.inventory:
			self.inventory[item]['quantity'] = 0
		self.carryLimit = 500
		self.level = level
		self.name = name

		self.icon = u"\U0001f355"

		# Sight radius This will later be a factor of player class
		self.sight=3
	def __repr__(self):
		out  = "Final Health : {0}\n".format(self.health)
		out += "Final Score  : {0}\n".format(self.score)
		out += "Ending Level : {0}\n".format(self.level)


	def setName(self,name):
		self.name = name

	def getName(self):
		return self.name

	def __setHealth__(self,health):
		self.health = health

	def __addHealth__(self,health):
		self.health += health

	def getInventory(self):
		return self.inventory

	def checkInventory(self,item):
		return item in inventory

	def __setScore__(self, score):
		self.score = score
		return self.score

	def addScore(self,score):
		self.score += score
		return self.score

	def getScore(self):
		return self.score

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
			self.inventory[item]['quantity'] = self.inventory[item]['max']
			self.addScore(self.inventory[item]['score'])
			return True
		else:
			self.inventory[item]['quantity'] += itemNum
			return True



