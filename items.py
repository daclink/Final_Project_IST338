###
# Drew A. Clinkenbeard
# items.py
# This is where items are quantified...
# 29 - April - 2014
#
###

from __future__ import unicode_literals

import locale
import codecs
from math import floor

class items():

	def __init__(self):
		locale.setlocale(locale.LC_ALL, '')
		code = locale.getpreferredencoding()
		

	def __repr__(self):
		# self.items= { 	'health':{'icon':u"\U0001f493",'position':1,'max':100,'current':100},
		# 				'money':{'icon':u"\U0001f4b0",'position':4,'max':100000,'current':0},
		# 				'food':{'icon':u"\U0001f371",'position':7,'max':10,'current':0},
		# 				'bomb':{'icon':u"\U0001F4a3",'position':10,'max':10,'current':3,'timer':4,'action':self.__get_bomb__,'score':5}
		locale.setlocale(locale.LC_ALL, '')
		code = locale.getpreferredencoding()
		items = self.getItems()
		foo = u""

		for x in items:
			foo += "%s \n" %(x)


		
		return foo

	@staticmethod
	def getItems() :
		"""
			used to list the available items.
			This probably needs an overhaul
		"""
		ret = {}
		ret['bombs'] = items.bombs()
		ret['gold'] = items.gold()
		ret['food'] = items.food()

		return ret


	
	@staticmethod
	def bombs():
		"""
			Returns a bomb dictionary.
		"""
		bombs = {
			"max":10,
			'weight':5,
			'score': 5,
			'icon':u"\U0001F4a3",
			'position':10,
			'timer':4
		}
		return bombs

	@staticmethod
	def gold():
		"""
		Returns a gold dictionary
		"""
		gold = {
			"max":10000,
			'weight':0,
			'score':1,
			'icon':u"\U0001f4b0",
			'position':4
		}
		return gold
	
	@staticmethod
	def food():
		"""
			returns a food dictionary
		"""
		food = {
			"max":10,
			'weight':1,
			'score':2,
			'position':7,
			'icon':u"\U0001f371",
			'power':0.25
		}
		return food

	@staticmethod
	def showIcon(item):
		"""
			used to print the icon of an object

			input: dictionary item['icon']: 'unicode character'

			output: prints an icon
		"""
		print item['icon'].encode('utf-8') 

	@staticmethod
	def dropNumber(item):
		"""
			The quantity of the item dropped.
			This will be used for enemies and chests
		"""
		return int(range(1,item['max']*.3))

