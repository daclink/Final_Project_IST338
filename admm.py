#Drew A. Clinkenbeard
#http://www.unicode.org/Public/emoji/1.0/full-emoji-list.html
#http://en.wikipedia.org/wiki/Maze_generation_algorithm
#https://docs.python.org/2/library/curses.html#textbox-objects

#import admm; reload(admm); from admm import *;mm()

"""TODO
Add ending condition
Add Character object
	Implement health
	Implement attack
		* Fist U0000270A
		* knife 1F52A
		* hammer 1F528
		* crossed swords 2694
	Implement Defense
		* Shield thing U0001F530
	Add items
		* Implement Inventory
Add enemies 
?Add pop-ups for leveling?
	*https://docs.python.org/2/library/curses.html#textbox-objects


Add Loading screen

Add save/load feature


"""

import sys
import random
import time
import curses
import locale
import random
import math
import json
from time import localtime, strftime
from inspect import currentframe, getframeinfo
# my classes
from items import *
import logger
import player

sys.setrecursionlimit(100000)

class mm():

	def __init__(self, score=0,debug=False):
		self.debug = debug
		self.log = logger.Logger("admm.log")

		self.log._log("testing...")
		maze = {}
		# self.maxY = y-1
		# self.maxX = x-1
		# self.minY = self.minX = 0
		self.visited = 0

		locale.setlocale(locale.LC_ALL, '')
		code = locale.getpreferredencoding()
		self.debug = debug
		if debug :
			print "Hello there! deubg is ", debug
		# Setup Player
		
		# pizza
		# player =	u"\U0001f355"

		# p1 = {
		# 		'player':player,
		# 		'inventory':{},
		# 		'items':{},
		# 		'sight': 3
		# 	}

		self.score = score
		p1 = player.Player()
		p1.addItem('bombs',3)
		self.__setScore__(self.score,p1)
		#house
		self.exit = u"\U0001f3e0"
		#blue thing
		# self.exit = u"\U0001f4a0"

		# Setup Screen
		stdscr = curses.initscr()
		curses.savetty() #make sure we can put the screen back the way we found it
		curses.noecho() #prevent keypresses appearing on screen
		curses.cbreak() #interpret input with out return
		stdscr.keypad(1) #everyone loves the keypad
		stdscr.clearok(1) #allow the screen to be cleared
		curses.curs_set(0) #hide the caret
		stdscr.border(0)

		curses.start_color()

		keypresses = { 
						'bomb':'b'
						,'quit':'q'
						# ,'menu':'m'
					}

		self.items= { 	'health':{'icon':u"\U0001f493",'position':1,'max':100,'current':100},
						'money':{'icon':u"\U0001f4b0",'position':4,'max':100000,'current':0},
						'food':{'icon':u"\U0001f371",'position':7,'max':10,'current':0},
						'bomb':{'icon':u"\U0001F4a3",'position':10,'max':10,'current':3,'timer':4,'action':self.__get_bomb__,'score':5}
				 	}
		# p1['items'] = self.items



		self.enemies = {}
		# used for placing on screen bombs
		sbomb = {}
		rem_bomb = []

		stdscr.clear()
		stdscr.refresh()

		self.minX = minX	= 0
		#how far to the right we can go.
		#Leaving room for messages.
		self.maxX = maxX	= stdscr.getmaxyx()[1] -15

		self.minY = minY	= 0
		##how far down we can go
		#leaving room for messages
		self.maxY = maxY	= stdscr.getmaxyx()[0] 


		# Room stuff
		self.maxRoomSize = 4
		self.roomY = []
		self.roomX = []
		for rooms in range(int((self.maxX*.25))):
			self.roomY += [random.choice(range(self.maxY))]
			self.roomX += [random.choice(range(self.maxX))]
		if debug:
			self.log._log("setting room up\nroomY numbers",getframeinfo(currentframe()).lineno,"low")
			self.log._log(json.dumps(self.roomY),getframeinfo(currentframe()).lineno,"low")
			

		self.uv = []

		# setup maze
		for cols in range(maxY):
			maze[cols] = {}
			
			for rows in range(maxX):
				maze[cols][rows] = {}
				maze[cols][rows]['wall'] = True
				maze[cols][rows]['visited'] = False
				maze[cols][rows]['checked'] = False
				maze[cols][rows]['contains'] = {}
				self.visited += 1
				self.uv.append([cols,rows])
				

		# self.lastY = 5
		# self.lastX = 25
		# self.startX = 70
		# self.startY = 100


		self.maze = maze
		self.__get_start__()
		self.maze[self.startY][self.startX]['contains'] = "exit"
		self.__generate_maze__(self.startY,self.startX)

		self.__make_room__(self.startY,self.startX,3)

		self.__get_player_start__()

		charPos = [self.lastY,self.lastX]
		self.__make_room__(charPos[0],charPos[1],3)

		self.__place_items__()

		# self.__hider__()
			
		#self.__reveal__(charPos[0],charPos[1],p1['sight'])

		stdscr.clear()
		stdscr.refresh()
		# begin main while

		self.moveTest = True
		# charPos = {'y':0,'x':0}
		while self.moveTest:

			stdscr.clear()

			for cols in self.maze:
				for rows in self.maze[cols]:
					# if self.maze[cols][rows]['visited']:
					if self.maze[cols][rows]['wall'] :
						stdscr.addstr(cols,rows,"#",curses.A_DIM)
					else:
						if self.maze[cols][rows]['checked']:
							stdscr.addstr(cols,rows,".",curses.A_DIM)
						else :
							stdscr.addstr(cols,rows," ",curses.A_DIM)
					for inv in self.maze[cols][rows]['contains']:
						try:
							if self.maze[cols][rows]['contains'][inv]:
								stdscr.addstr(cols,rows,self.items[inv]['icon'].encode("utf-8"))
						except Exception as e:
							# print  self.maze[cols][rows]['contains']
							msg = "inventory is {0}".format(self.maze[cols][rows]['contains'])
							
							self.log._err(e,msg,"212","medium")
					# else :
					# 	stdscr.addstr(cols,rows,".",curses.A_DIM)
			stdscr.addstr(charPos[0],charPos[1]-1,p1.icon.encode("utf-8"))
			# display side items
			stdscr.addstr(self.minY,self.maxX+2,"Score")
			stdscr.addstr(self.minY+1,self.maxX +2,str(self.score))
			for item in items.getItems():
				posY = self.minY + items.getItems()[item]['position'] + 3
				posX = self.maxX + 2  #guh magic number
				# icon = self.items[item]['icon']
				# values += " 
				msg = "Trying to get the inventory to display properly...\n"
				msg += " p1.inventory == {0}".format(p1.inventory) 
				self.log._log(msg,226)
				values = str(p1.inventory[item]['quantity'])
				values += "/"
				values += str(items.getItems()[item]['max'])

				name =  item
				name += " "
				name += items.getItems()[item]['icon']

				stdscr.addstr(posY,posX,name.encode("utf-8"))
				stdscr.addstr(posY+1,posX,values.encode("utf-8"))


			stdscr.addstr(self.startY,self.startX,self.exit.encode("utf-8"))

			for b in sbomb:
				sbomb[b]['counter'] -= 1
				if sbomb[b]['counter'] < 0:
					rem_bomb +=[b]
			if rem_bomb:
				for b in rem_bomb:
					self.__det_bomb(sbomb[b])
					del sbomb[b]
				rem_bomb = []
			if sbomb:						
				for b in sbomb:
					stdscr.addstr(sbomb[b]['y'],sbomb[b]['x'],self.items['bomb']['icon'].encode("utf-8"), curses.A_BLINK)
					stdscr.addstr(sbomb[b]['y'],sbomb[b]['x']+1,str(sbomb[b]['counter']))

			stdscr.refresh()
			move = stdscr.getch()
			if move == ord('q') or move == ord('Q') :
				self.moveTest = False
			elif move == ord('b') or move == ord('B') :
				self.__place_bomb__(charPos[0],charPos[1],sbomb,p1)

			elif move == curses.KEY_RIGHT:
				if self.maze[charPos[0]][charPos[1]+1]['wall'] == False :
					charPos[1] += 1
			elif move == curses.KEY_LEFT:
				if self.maze[charPos[0]][charPos[1]-1]['wall'] == False :
					charPos[1] -= 1
			elif move == curses.KEY_UP:
				if self.maze[charPos[0]-1][charPos[1]]['wall'] == False :
					charPos[0] -= 1
			elif move == curses.KEY_DOWN:
				if self.maze[charPos[0]+1][charPos[1]]['wall'] == False :
					charPos[0] += 1
			
			self.__reveal__(charPos[0],charPos[1],p1.sight)
			
			self.__cell_check__(charPos[0],charPos[1],p1)

			self.score = p1.score

		# end main while


		time.sleep(1)
		##put it all back
		curses.resetty()
		curses.endwin()

	def __reveal__(self,y,x,sight):

		for cols in range(y-sight,y+sight):
			for rows in range(x-sight,x-sight):
				if self.__in_range__(cols,rows) and self.maze[cols][rows]['visited']:
					self.maze[cols][rows]['visited'] = True
					self.__addScore__(1,p1)

	def __get_start__(self):
		self.startX = random.choice(range((self.minX+5),(self.maxX-5)))
		self.startY = random.choice(range((self.minY+5),(self.maxY-5)))

	def __get_player_start__(self,y=-1,x=-1):
		
		if y == -1 and x == -1:
			y = abs(self.maxY - self.startY)
			x = abs(self.maxX - self.startX)
		
		neighbors = {}

		if self.maze[y][x]['wall'] or not self.__in_range__(y,x):
			neighbors = self.__get_neighbor__(y,x)
		else:
			self.lastY = y
			self.lastX = x
			return
		try :
			if not neighbors:
				self.__get_player_start__(random.choice(range(y)),random.choice(range(x)))
				return 
		except :
			msg = "Neighbors = " , neighbors
			self.log._log(msg, "293","Low")

		try :
			for n in neighbors:
				y = neighbors[n]['y']
				x = neighbors[n]['x']
				if self.__in_range__(y,x) and not self.maze[y][x]['wall']:
					self.lastY = y
					self.lastX = x
					return
		except :
			msg = "Neighbors = " , neighbors
			self.log._log(msg, "301","Low")
		if neighbors:
			n = random.choice(neighbors.keys())
			self.__get_player_start__(neighbors[n]['y'],neighbors[n]['x'])
		else:
			self.__get_player_start__(random.choice(range(y)),random.choice(range(x)))
			return 


		return 


	def __cell_check__(self,y,x,p):

		if not self.maze[y][x]['checked']:
			self.maze[y][x]['checked'] = True
			self.__addScore__(1,p)
		if self.maze[y][x]['contains']:
			for item in self.maze[y][x]['contains']:
				if item in self.items:
					if self.maze[y][x]['contains'][item]:
						self.items[item]['action'](y,x,p)

				if item in self.enemies:
					self.enemies[item]['encounter'](y,x)
		if y == self.startY and x == self.startX:
			self.__found_exit__()

				

	def __found_exit__(self):
		self.moveTest = False

	def __repr__(self):
		maze = ''
		checked = 0
		total = 0
		for cols in self.maze:
			for rows in self.maze[cols]:
				if self.maze[cols][rows]['wall'] :
					# print '.',
					maze += '#'
				else:
					if self.maze[cols][rows]['checked']:
						# print ' ',
						checked +=1
						maze += '.'
					else :
						total +=1
						maze += ' '

			# print '\n'
			maze += '\n'
		total = total + checked

		maze += "Final Score =   %d\n" %(self.score)
		maze += "Squares Seen  : %d \n" %(checked)
		maze += "Total Squares : %d \n" %(total)
		checked = checked *1.0
		total = checked/total
		total = total * 100.00
		maze += "Explored Percent = %.2f" %(total)
		maze += "%"


		return maze


	def __get_neighbor__(self,y,x,diagonals=False):
		neighbors = {}
		# check north and northwest cells
		if (y-2) >= self.minY and not self.maze[y-2][x]['visited']:
			neighbors['N'] = {'y':y-2,'x':x} 
			if diagonals and x-2 >= self.minX:
				neighbors['NW'] = {'y':y-2,'x':x-2}

		# check east and south east
		if (x+2) <= self.maxX-1 and not self.maze[y][x+2]['visited']:
			neighbors['E'] = {'y':y,'x':x+2}
			if diagonals and (y+2) <= self.maxY:
				neighbors['SE'] = {'y':y+2,'x':x+2} 

		# check the north and nw corners
		if (x-2) >= self.minX and not self.maze[y][x-2]['visited']:
			neighbors['W'] = {'y':y,'x':x-2}
			if diagonals and (y-2) >= self.minY:
				neighbors['NW'] = {'y':y-2,'x':x-2}

		# check south cell and south west cell
		if (y+2) <= self.maxY-1 and not self.maze[y+2][x]['visited']:
			neighbors['S'] = {'y':y+2,'x':x}
			# check southwest cell
			if diagonals and x+2 <= self.maxX:
				neighbors['SW'] = {'y':y+2,'x':x+2}
		# print neighbors
		return neighbors

	def __generate_maze__(self,y,x,load=False):

		load = self.__get_window__()
		load.box()
		load.clear()
		li = ['\\','-','/','|']
		message = "Generating Maze"
		message += " "
		message += str(self.visited)
		message += " "
		message += li[self.visited%4]
		load.addstr(0,0,message.encode("utf-8"))
		load.refresh()

		self.maze[y][x]['wall']= False
		self.maze[y][x]['visited'] = True
		self.visited += 1

		neighbors = self.__get_neighbor__(y,x)
		self.lastY = y
		self.lastX = x

		while neighbors:
			rand_neighbor = random.choice(neighbors.keys())

			try :
				ny = neighbors[rand_neighbor]['y']
				nx = neighbors[rand_neighbor]['x']
			except KeyError as e:
				if debug:
					self.log._err(e,{'x':x,'y':y,'ny':ny,'nx':nx,'report':"getting neighbors of x and y"},getframeinfo(currentframe()).lineno)

			if self.__in_range__(ny,nx) and not self.maze[ny][nx]['visited']:
				

				if ny == random.choice(range(self.maxY)):
					self.__make_room__(ny,nx,random.choice(range(self.maxRoomSize)))

				if (ny - y) > 0:
					self.maze[ny-1][x]['visited'] = True
					self.maze[ny-1][x]['wall'] = False
					self.visited += 1
				if (ny - y) < 0:
					self.maze[ny+1][x]['visited'] = True
					self.maze[ny+1][x]['wall'] = False
					self.visited += 1
				if (nx - x) > 0:
					self.maze[y][nx-1]['visited'] = True
					self.maze[y][nx-1]['wall'] = False
					self.visited += 1
				if (nx - x) < 0:
					self.maze[y][nx+1]['visited'] = True
					self.maze[y][nx+1]['wall'] = False
					self.visited += 1
			del neighbors[rand_neighbor]

			self.__generate_maze__(ny,nx)

			if self.visited > 0:
				self.__generate_maze__(ny,nx)

			rm = random.choice(range(10,42))
			while rm > 0 and self.roomY and self.roomX:
				rmy = self.roomY.pop()
				rmx = self.roomX.pop()
				self.__make_room__(rmy,rmx)
				rm -=1

			# add a border
		for col in self.maze:
			self.maze[col][self.minX]['visited'] = True
			self.maze[col][self.minX]['wall'] = True
			self.maze[col][self.maxX-1]['visited'] = True
			self.maze[col][self.maxX-1]['wall'] = True

		for row in self.maze[col]:
			self.maze[self.minY][row]['visited'] = True
			self.maze[self.minY][row]['wall'] = True
			self.maze[self.maxY-1][row]['visited'] = True
			self.maze[self.maxY-1][row]['wall'] = True



		# load.endwin()

		return 0

	def __hider__(self):
		for col in range(self.maxY):
			for row in range(self.maxX):
				if self.__in_range__(col,row):
					self.maze[col][row]['visited'] = False

	def __setScore__(self, score,p):
		p.score = score

	def __addScore__(self,score,p):
		p.score = p.score + score

	def __place_items__(self):

		
		for x in range(random.choice(range(3,6))):
			
			y = random.choice(range(self.maxY))
			x = random.choice(range(self.maxX))
			while self.maze[y][x]['wall']:
				y = random.choice(range(self.maxY))
				x = random.choice(range(self.maxX))
			
			self.maze[y][x]['contains']['bomb'] = True


	def __make_room__(self,y,x,size=-1):
		# neighbors = self.__get_neighbor__(y,x)
		# I wanted to use list comprehension...
		# self.maxRoomSize+1 to account for the way range works
		# self.log.write("what?!\n\n")
		# json.dump(neighbors,self.log)
		msg = "calling make_room with y=%d,x=%d,size=%d" %(y,x,size)
		if self.debug:
			self.log._log(msg,"489")
		
		if size < 1:
			size = random.choice(range(1,self.maxRoomSize))
		if self.debug:
			msg = "making a room with\n Y: %d - %d \n \nx: %d - %d" %(y-size, y+size+1,x-size,x+size+1)
			self.log._log(msg,"551")
		for cols in range(y-size,y+size):
			for rows in range(x-size,x+size):
				try:
					if self.__in_range__(cols,rows):
						if not self.maze[cols][rows]['visited']:
							self.maze[cols][rows]['visited'] = True
							self.visited += 1
						self.maze[cols][rows]['wall'] = False
				except KeyError as e:
					values = {"cols":cols,"rows":rows}
					if debug:
						self.log._err(e,values,"563")


	def __place_bomb__(self,y,x,sbomb,p):
		if p.inventory['bombs']['quantity'] > 0:
			p.inventory['bombs']['quantity'] -= 1
			sbomb[len(sbomb)+1] = {'counter':self.items['bomb']['timer'],'y':y,'x':x}
		

	def __get_item__(self,y,x,item):
		pass
		# check item capacity
		# add item up to capacity
		# mark maze item as gone

	def __det_bomb(self,bomb):
		for col in range(bomb['y']-1,bomb['y']+2):
			for row in range(bomb['x']-1,bomb['x']+2):
				if self.__in_range__(col,row):
					self.maze[col][row]['wall'] = False


	def __get_bomb__(self,y,x,p):
		self.maze[y][x]['contains']['bomb'] = False
		p.inventory['bombs']['quantity'] += 3
		self.__addScore__(self.items['bomb']['score'],p)

	def __in_range__(self,y,x):
		"""
			check if the y and x values are in screen range
			+/- 1 to account for the screen border.
		"""
		return self.minY < y < self.maxY-1 and self.minX < x < self.maxX-1


	def __get_window__(self,size="small"):
		if size.lower() == 'small':
			startY = int(self.maxY*.5)
			startX = int(self.maxX*.5)
			endY   = int(self.maxY*.1)
			endX   = int(self.maxX*.1)
			return curses.newwin(startY,startX,endY,endX)
		else :
			startY = int(self.maxY*.5)
			startX = int(self.maxX*.5)
			endY   = int(self.maxY*.1)
			endX   = int(self.maxX*.1)
			return curses.newwin(self.maxY*.5,self.maxX*.5,self.maxY*.25,self.maxX*.25)
