#Drew A. Clinkenbeard
#http://www.unicode.org/Public/emoji/1.0/full-emoji-list.html
#http://en.wikipedia.org/wiki/Maze_generation_algorithm
#https://docs.python.org/2/library/curses.html#textbox-objects

#import admm; reload(admm); from admm import *

"""TODO
Add ending condition
Implement health
Implement attack
	* Fist U0000270A
	* knife 1F52A
	* hammer 1F528
	* crossed swords 2694
Implement Defense
	* Shield thing U0001F530
Add enemies 
Add items
	* Implement Inventory

?Add pop-ups for leveling?
	*https://docs.python.org/2/library/curses.html#textbox-objects


Add Loading screen

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

sys.setrecursionlimit(100000)
class mm():

	def __init__(self, debug=True):
		self.debug = debug
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
		self.setScore(0)
		# pizza
		player =	u"\U0001f355"

		#house
		# self.exit = u"\U0001f3e0"
		self.exit = u"\U0001f4a0"

		# Setup Screen
		stdscr = curses.initscr()
		curses.savetty() #make sure we can put the screen back the way we found it
		curses.noecho() #prevent keypresses appearing on screen
		curses.cbreak() #interpret input with out return
		stdscr.keypad(1) #everyone loves the keypad
		stdscr.clearok(1) #allow the screen to be cleared
		curses.curs_set(0) #hide the caret

		curses.start_color()

		keypresses = { 
						'bomb':'b'
						,'quit':'q'
						# ,'menu':'m'
					}

		self.items= { 	'health':{'icon':u"\U0001f493",'position':1,'max':100,'current':100},
						'money':{'icon':u"\U0001f4b0",'position':4,'max':100000,'current':0},
						'food':{'icon':u"\U0001f371",'position':7,'max':10,'current':0},
						'bomb':{'icon':u"\U0001F4a3",'position':10,'max':10,'current':3,'timer':4}
				 	}
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
			self.__logger__("setting room up\nroomY numbers",getframeinfo(currentframe()).lineno,"low")
			self.__logger__(json.dumps(self.roomY),getframeinfo(currentframe()).lineno,"low")
			

		self.uv = []

		# setup maze
		for cols in range(maxY):
			maze[cols] = {}
			
			for rows in range(maxX):
				maze[cols][rows] = {}
				maze[cols][rows]['wall'] = True
				maze[cols][rows]['visited'] = False
				self.visited += 1
				self.uv.append([cols,rows])
				

		# self.lastY = 5
		# self.lastX = 25
		# self.startX = 70
		# self.startY = 100


		self.maze = maze
		self.__get_start__()
		self.__generate_maze__(self.startY,self.startX)

		self.__make_room__(self.startY,self.startX,3)

		self.__get_player_start__()

		charPos = [self.lastY,self.lastX]
		self.__make_room__(charPos[0],charPos[1],3)

		stdscr.clear()
		stdscr.refresh()
		# begin main while

		moveTest = True
		# charPos = {'y':0,'x':0}
		while moveTest:

			stdscr.clear()

			for cols in self.maze:
				for rows in self.maze[cols]:
					if self.maze[cols][rows]['wall'] :
						stdscr.addstr(cols,rows,"#",curses.A_DIM)
			stdscr.addstr(charPos[0],charPos[1]-1,player.encode("utf-8"))
			# display side items
			for item in self.items:
				posY = self.minY + self.items[item]['position'] + 1
				posX = self.maxX + 1  #guh magic number
				# icon = self.items[item]['icon']
				# values += " " 
				values = str(self.items[item]['current'])
				values += "/"
				values += str(self.items[item]['max'])

				name =  item
				name += " "
				name += self.items[item]['icon']

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
				moveTest = False
			elif move == ord('b') or move == ord('B') :
				self.__place_bomb__(charPos[0],charPos[1],sbomb)

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
			
			
			self.__space__(charPos[0],charPos[1])

		# end main while


		time.sleep(1)
		##put it all back
		curses.resetty()
		curses.endwin()


	def __get_start__(self):
		self.startX = random.choice(range((self.minX+5),(self.maxX-5)))
		self.startY = random.choice(range((self.minY+5),(self.maxY-5)))

		# self.startY = random.choice(self.maze.keys())
		# self.startX = random.choice(self.maze[self.startY].keys())
		# self.__make_room__(self.startY,self.startX,0)

	def __get_player_start__(self,y=-1,x=-1):
		
		if y == -1 and x == -1:
			y = abs(self.maxY - self.startY)
			x = abs(self.maxX - self.startX)
		
		if self.maze[y][x]['wall']:
			neighbors = self.__get_neighbor__(y,x)
		else:
			self.lastY = y
			self.lastX = x
			return

		for n in neighbors:
			y = neighbors[n]['y']
			x = neighbors[n]['x']
			if self.__in_range__(y,x)  and not self.maze[y][x]['wall']:
				self.lastY = y
				self.lastX = x
				return
		n = random.choice(neighbors.key())

		__get_player_start__(neighbors[n]['y'],neighbors[n]['x'])

		return 
		


	def __space__(self,y,x):
		pass

	def __repr__(self):
		maze = ''
		for cols in self.maze:
			for rows in self.maze[cols]:
				if self.maze[cols][rows]['wall'] :
					# print '.',
					maze += '#'
				else:
					# print ' ',
					maze += ' '
			# print '\n'
			maze += '\n'

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

	def __generate_maze__(self,y,x):

		self.maze[y][x]['wall']= False
		self.maze[y][x]['visited'] = True
		self.visited -= 1

		neighbors = self.__get_neighbor__(y,x)
		self.lastY = y
		self.lastX = x

		while neighbors:
			rand_neighbor = random.choice(neighbors.keys())

			try :
				ny = neighbors[rand_neighbor]['y']
				nx = neighbors[rand_neighbor]['x']
			except KeyError as e:
				self.__err__(e,{'x':x,'y':y,'ny':ny,'nx':nx,'report':"getting neighbors of x and y"},getframeinfo(currentframe()).lineno)

			if self.__in_range__(ny,nx) and not self.maze[ny][nx]['visited']:
				# self.visited -= 1

				if ny == random.choice(range(self.maxY)):
					self.__make_room__(ny,nx,random.choice(range(5)))

				if (ny - y) > 0:
					self.maze[ny-1][x]['visited'] = True
					self.maze[ny-1][x]['wall'] = False
				if (ny - y) < 0:
					self.maze[ny+1][x]['visited'] = True
					self.maze[ny+1][x]['wall'] = False
				if (nx - x) > 0:
					self.maze[y][nx-1]['visited'] = True
					self.maze[y][nx-1]['wall'] = False
				if (nx - x) < 0:
					self.maze[y][nx+1]['visited'] = True
					self.maze[y][nx+1]['wall'] = False
			del neighbors[rand_neighbor]

			self.__generate_maze__(ny,nx)

			if self.visited > 0:
				self.__generate_maze__(ny,nx)

			# Old random room code...
			# for ry in self.roomY:
			# 	for rx in self.roomX:
			# 		self.__make_room__(ry,rx,self.maxRoomSize)
			# NEW random room code...
			# msg = "length of roomY %d, length of roomX %d)" %(len(self.roomY),len(self.roomX))
			# self.__logger__(msg,"355")
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

		return 0


	def setScore(self, score):
		self.score = score


	def __make_room__(self,y,x,size=-1):
		# neighbors = self.__get_neighbor__(y,x)
		# I wanted to use list comprehension...
		# self.maxRoomSize+1 to account for the way range works
		# self.log.write("what?!\n\n")
		# json.dump(neighbors,self.log)
		msg = "calling make_room with y=%d,x=%d,size=%d" %(y,x,size)
		if self.debug:
			self.__logger__(msg,getframeinfo(currentframe()).lineno)
		
		if size < 1:
			size = random.choice(range(1,self.maxRoomSize))
		if self.debug:
			msg = "making a room with\n Y: %d - %d \n \nx: %d - %d" %(y-size, y+size+1,x-size,x+size+1)
			self.__logger__(msg,getframeinfo(currentframe()).lineno)
		for cols in range(y-size,y+size):
			for rows in range(x-size,x+size):
				try:
					if self.__in_range__(cols,rows):
						if not self.maze[cols][rows]['visited']:
							self.maze[cols][rows]['visited'] = True
							self.visited -= 1
						self.maze[cols][rows]['wall'] = False
				except KeyError as e:
					values = {"cols":cols,"rows":rows}
					self.__err__(e,values,"394")


			
		# if size > 0:
		# 	for r in neighbors:
		# 		self.__make_room__(neighbors[r]['y'],neighbors[r]['x'],size-1)	
		# else:
		# 	for r in neighbors:
		# 		if not self.maze[neighbors[r]['y']][neighbors[r]['x']]['visited']:
		# 			self.maze[neighbors[r]['y']][neighbors[r]['x']]['visited']=True
		# 			self.visited -= 1
		# 		self.maze[neighbors[r]['y']][neighbors[r]['x']]['wall'] = False


	def __place_bomb__(self,y,x,sbomb):
		if self.items['bomb']['current'] > 0:
			self.items['bomb']['current'] -= 1
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


	def __in_range__(self,y,x):
		"""
			check if the y and x values are in screen range
			+/- 1 to account for the screen border.
		"""
		return self.minY < y < self.maxY-1 and self.minX < x < self.maxX-1

	def __err__(self,e,values,line):
		log =  open("admm.log",'a')
		stats  = "minY %d maxY %d\n" %(self.minY, self.maxY)
		stats += "minX %d maxX %d\n" %(self.minX, self.maxX)
		stats += "len(self.maze) %d len(self.maze[self.minY]) %d" %(len(self.maze) , len(self.maze[self.minY]))

		report = strftime("[%d.%b.%Y %H:%M:%S] ",localtime())
		report += 'KeyError: ['
		report += str(e)
		report += ']\n'
		log.write(report)
		log.write("\n**stats**\n")
		log.write(stats)
		log.write("\n**stats**\n")
		log.write("\n ** report **\n")
		json.dump(values,log)
		log.write("\n ** report **\n")
		log.close()

	def __logger__(self,msg,line="none",level="Low"):
		log =  open("admm.log",'a')
		log.write("=-=-= Log Level: %s  =-=-=-=\n" %(level))
		log.write(strftime("[%d.%b.%Y %H:%M:%S] \n ",localtime()))
		log.write("line : \t %s \n" %(str(line)))
		log.write("message: \t")
		log.write(msg)
		log.write("\n=-=-=-=-=-=-=-=-=-=-=-=\n")
		log.close()
		
		
# maze = maze_maker()

# print maze.maze

# maze

