###
# Drew A. Clinkenbeard
# enemy.py
# used to create enemies
# 2 - May - 2014
#
###

import random
from math import ceil

import items

class Enemy():


			

	def __init__(self, etype=-1, level=1):
		"""
			used to spawn an enemy. 

			Inputs: char/int etype: the type of enemy to spawn. -1 == random. 
					Default:-1
					
					int level: the level of the monster. This is relative 
					to the player facing the monster
					Default 1
		"""
		self.level=level
		self.enemy_list = {
			'kobold':self.kobold,
			'rat':self.rat
			}

		if etype < 0 :
			etype = random.choice(self.enemy_list.keys())

		self.enemy_list[etype]()

	def __repr__(self):

		ret = self.etype + "\n"
		ret += "level: {0}\n".format(self.level)
		ret += "HP:    {0}\n".format(self.hp)
		ret += "att:   {0}\n".format(self.attack)
		ret += "def:   {0}\n".format(self.defense)
		ret += "drops: {0}\n".format(self.drop)
		ret += "=-=-=-=-=-=-=-=-=\n"
		ret += "XP earned {0}\n".format(self.xp)

		return ret

	def kobold(self):
		self.etype = "kobold"
		self.level = int(ceil(self.level*.5))
		self.xp = self.level*2
		self.attack = self.level*random.choice(range(1,6))
		self.defense = self.level*random.choice(range(1,6))
		self.hp = self.level*random.choice(range(1,10))
		
		self.drop = random.choice(items.items.getItems().keys())


	def rat(self):
		self.etype = "rat"
		self.level = int(ceil(self.level*.5))
		self.xp = self.level*2
		self.attack = self.level*random.choice(range(1,6))
		self.defense = self.level*random.choice(range(1,6))
		self.hp = self.level*random.choice(range(1,10))
		self.drop = random.choice(items.items.getItems().keys())


k = Enemy(-1,15)

print k


