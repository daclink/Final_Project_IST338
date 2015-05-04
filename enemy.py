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
		"""
			I know I could just make this one big format
			String but I don't want too.
		"""

		ret  = u"{0} {1}\n".format(self.etype, self.icon)
		ret += u"level:\t{0}\n".format(self.level)
		ret += u"HP:\t{0}\n".format(self.hp)
		ret += u"att:\t{0}\n".format(self.attack)
		ret += u"def:\t{0}\n".format(self.defense)
		# ret += u"XP:\t{0}\n".format(self.xp)
		ret += u"drops:\t{0}\n".format(self.drop)
		ret += u"=-=-=-=-=-=-=-=-=\n"
		ret += u"XP earned {0}\n".format(self.xp)

		return ret.encode("utf-8")

	def kobold(self):
		self.etype 		= u"kobold"
		self.level 		= int(ceil(self.level*.5))
		self.xp 		= self.level*2 + random.choice(range(1,7))
		self.attack 	= self.level*random.choice(range(1,6))
		self.defense 	= self.level*random.choice(range(1,6))
		self.hp 		= self.level*random.choice(range(1,10))		
		self.drop 		= random.choice(items.items.getItems().keys())
		self.icon 		= u"\U0001f409"


	def rat(self):
		self.etype 		= u"rat"
		self.level 		= int(ceil(self.level*.5))
		self.xp 		= self.level*2 + random.choice(range(1,5))
		self.attack 	= self.level*random.choice(range(1,6))
		self.defense	= self.level*random.choice(range(1,6))
		self.hp 		= self.level*random.choice(range(1,10))
		self.drop 		= random.choice(items.items.getItems().keys())
		self.icon 		= u"\U0001f400"



