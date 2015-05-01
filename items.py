# This is where items are quantified...
from __future__ import unicode_literals

import locale
import codecs

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
		items = self.items()
		foo = u""
		# foo = "\U0001F4a3".encode("utf-8")
		# foo = "\xF0\x9F\x92\xA3".encode("utf-8")
		for x in items:
			foo += "%s \n" %(x)
			# for y in items[x]:
			# 	if y != 'icon':
			# 		foo += "\t {0} : {1} \n ".format(y,items[x][y])
			# 	# foo += '\t %s : %s \n' %(y,unicode(items[x][y]))


		
		return foo

	@staticmethod
	def getItems() :
		ret = {}
		ret['bombs'] = items.bombs()
		ret['gold'] = items.gold()
		ret['food'] = items.food()

		return ret


	
	@staticmethod
	def bombs():
		# 'bomb':{
				# 'icon':u"\U0001F4a3",
				# 'position':10,
				# 'max':10,
				# 'current':3,
				# 'timer':4,
				# 'action':self.__get_bomb__,
				# 'score':5
				# }
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
		# 'icon':u"\U0001f4b0",'position':4,'max':100000,'current':0}
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
		# 'food':{'icon':u"\U0001f371",'position':7,'max':10,'current':0},
		food = {
			"max":10,
			'weight':1,
			'score':2,
			'position':7,
			'icon':u"\U0001f371"
		}
		return food

	@staticmethod
	def showIcon(item):
		print item['icon'].encode('utf-8') 

