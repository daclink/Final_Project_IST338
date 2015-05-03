###
# Drew A. Clinkenbeard
# Advanced Maze Maker
# and main game loop....
# 14 - April - 2014
#
###
#=-=-=-=-= sources -=-=-=-=-=-
#http://www.unicode.org/Public/emoji/1.0/full-emoji-list.html
#http://en.wikipedia.org/wiki/Maze_generation_algorithm
#https://docs.python.org/2/library/curses.html
###

#import admm; reload(admm); from admm import *;mm()

"""TODO
Add Character object
	Implement attack
		* Fist U0000270A
		* knife 1F52A
		* hammer 1F528
		* crossed swords 2694
	Implement Defense
		* Shield thing U0001F530
Add enemies 
?Add pop-ups for leveling?
	*https://docs.python.org/2/library/curses.html#textbox-objects

=-=-=-=-=-= WAY Future features

Add save/load feature
Add multiplayer


"""

import sys
import random
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
		"""
			admm started out as JUST the maze maker (ADvanced Maze Maker)
			but it sort of spiraled out of control. It is currently the 
			main game loop as well. I am not sure if I will ever change that.
			It takes a score and a debug value.
			I noticed that debug was, possibly, leading to segfaults...

			Inputs: int: 		score 
					boolean:	debug
			Output: Not really much

		"""
		self.debug = debug
		self.log = logger.Logger("admm.log")

		
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
		
		# exit icon
		#red circle?
		# self.exit =u"\U00002B55"
		#hot springs
		# self.exit =u"\U00002668"
		#house
		# self.exit = u"\U0001f3e0"
		#blue thing
		self.exit = u"\U0001f4a0"
		# arrow?
		# self.exit = u"\U000023eb"

		#wall Icon
		self.wall = "#"

		# self.wall = u"\U00002B1C"

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
			

		# setup maze
		# 
		for cols in range(maxY):
			maze[cols] = {}
			
			for rows in range(maxX):
				maze[cols][rows] = {}
				maze[cols][rows]['wall'] = True
				maze[cols][rows]['visited'] = False
				maze[cols][rows]['checked'] = False
				maze[cols][rows]['contains'] = {}
				self.visited += 1


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

		# OH my goodness this is such a hack
		# this started life as a way to test character movement...
		# it is currently the main game loop... >_<

		self.moveTest = True
		# charPos = {'y':0,'x':0}
		while self.moveTest:

			stdscr.clear()

			for cols in self.maze:
				for rows in self.maze[cols]:
					if self.maze[cols][rows]['wall'] :
						stdscr.addstr(cols,rows,self.wall.encode("utf-8"),curses.A_DIM)
					else:
						if self.maze[cols][rows]['checked']:
							stdscr.addstr(cols,rows,".",curses.A_DIM)
						else :
							stdscr.addstr(cols,rows," ",curses.A_DIM)
					for inv in self.maze[cols][rows]['contains']:
						try:
							if inv in self.items and self.maze[cols][rows]['contains'][inv]:
								stdscr.addstr(cols,rows,self.items[inv]['icon'].encode("utf-8"),curses.A_NORMAL)
						except Exception as e:
							# print  self.maze[cols][rows]['contains']
							msg = "inventory is {0}".format(self.maze[cols][rows]['contains'])
							
							self.log._err(e,msg,"219","medium")
			
			# Drawing the player character.
			# eventually the charPos should PROBABLY be contained in the 
			# player object... I will add it to the list.
			stdscr.addstr(charPos[0],charPos[1]-1,p1.icon.encode("utf-8"))
			
			# display side items
			stdscr.addstr(self.minY,self.maxX+2,"Score")
			stdscr.addstr(self.minY+1,self.maxX +2,str(p1.score))
			for item in items.getItems():
				posY = self.minY + items.getItems()[item]['position'] + 3
				posX = self.maxX + 2  #guh magic number

				# Ditching this log statement because I think I fixed it...
				# msg = "Trying to get the inventory to display properly...\n"
				# msg += " p1.inventory == {0}".format(p1.inventory) 
				# self.log._log(msg,226)
				values = str(p1.inventory[item]['quantity'])
				values += "/"
				values += str(items.getItems()[item]['max'])

				name =  item
				name += " "
				name += items.getItems()[item]['icon']

				stdscr.addstr(posY,posX,name.encode("utf-8"))
				stdscr.addstr(posY+1,posX,values.encode("utf-8"))

				# okay here we are getting the list of keypresses.
				# one day I might add standard wasd keys for movement... 
				# note the offset for maxY...
				instOffset = len(keypresses)*2
				stdscr.addstr(self.maxY-instOffset,self.maxX+1, "Controls:")
				# self.log._log("offset = {0}".format(instOffset))
				for k in keypresses:
					instOffset -= 1
					cy = self.maxY-instOffset
					cx = self.maxX+2
					ctrl = "{0} = {1}".format(keypresses[k],k)
					# self.log._log(ctrl)
					stdscr.addstr(cy,cx,ctrl.encode("utf-8"))


			# Draw the exit
			stdscr.addstr(self.startY,self.startX,self.exit.encode("utf-8"), curses.A_NORMAL)

			# this should probably be its own functions
			# Currently this is how to calculate bomb detonations..
			# it is REALLY hacky.
			for b in sbomb:
				sbomb[b]['counter'] -= 1
				if sbomb[b]['counter'] < 0:
					rem_bomb +=[b]
			if rem_bomb:
				for b in rem_bomb:
					self.__det_bomb(sbomb[b],stdscr)
					del sbomb[b]
				rem_bomb = []
			if sbomb:						
				for b in sbomb:
					stdscr.addstr(sbomb[b]['y'],sbomb[b]['x'],self.items['bomb']['icon'].encode("utf-8"), curses.A_BLINK)
					stdscr.addstr(sbomb[b]['y'],sbomb[b]['x']+1,str(sbomb[b]['counter']))

			# okay we have drawn everything, time to make it show up.
			stdscr.refresh()

			# this is the movement loop.
			# I suspect there is a prettier way to do this but...

			move = stdscr.getch()
			if move == ord('q') or move == ord('Q') :
				self.moveTest = False
			elif move == ord('b') or move == ord('B') :
				self.__place_bomb__(charPos[0],charPos[1],sbomb,p1)

			elif move == curses.KEY_RIGHT or move == ord('d'):
				if self.maze[charPos[0]][charPos[1]+1]['wall'] == False :
					charPos[1] += 1
			elif move == curses.KEY_LEFT or move == ord('a'):
				if self.maze[charPos[0]][charPos[1]-1]['wall'] == False :
					charPos[1] -= 1
			elif move == curses.KEY_UP or move == ord('w'):
				if self.maze[charPos[0]-1][charPos[1]]['wall'] == False :
					charPos[0] -= 1
			elif move == curses.KEY_DOWN or move == ord('s'):
				if self.maze[charPos[0]+1][charPos[1]]['wall'] == False :
					charPos[0] += 1
			
			# This is currently disabled. 
			# there was a time where I had sight radius implemented.
			# that time may come again.
			# self.__reveal__(charPos[0],charPos[1],p)
			
			# check to see if there is anything in our cell.
			# I might make this check adjacent cells.. I might not.
			self.__cell_check__(charPos[0],charPos[1],p1)

			self.score = p1.score

		# end main while

		# time.sleep(1)
		
		##put it all back
		# The resetty() returns the terminal to standard 
		curses.resetty()
		# kill the window.
		curses.endwin()

	def __reveal__(self,y,x,p):
		"""
		Used to reveal a section of the map.
		Ideally this would be used to calculate how many squares to check
		Basically this is 'fog' to prevent overworking the CPU
		Also to add some mystery.
		It is currently broken.
		inputs: int y, the y coordinate
				int x, the x coordinate
				Player p, a player object
		output: modifies the visible cells. It is currently phenomenally broken.
		"""

		for cols in range(y-p.sight,y+p.sight):
			for rows in range(x-p.sight,x-p.sight):
				if self.__in_range__(cols,rows) and self.maze[cols][rows]['visited']:
					self.maze[cols][rows]['visited'] = True
					self.__addScore__(1,p)

	def __get_start__(self):
		"""
			generates the starting position of the maze.
			Ironically this is where the exit goes... >_< 
			A re-factor may be needed
			Since this is maze specific I felt it belonged in this object
			inputs:	none
			outputs: modifies the self.startY and self.startX values
		"""
		self.startX = random.choice(range((self.minX+5),(self.maxX-5)))
		self.startY = random.choice(range((self.minY+5),(self.maxY-5)))

	def __get_player_start__(self,y=-1,x=-1):
		"""
			finds the starting position of the player.
			This was tedious. I wanted it to be far enough away from the exit
			but I also wanted it to be random.
			I still get errors when it has trouble calculating the neighbors...
			I think that is a problem with my neighbor calculator.
			Totally. I forgot neighbors checks for visited cells..

			Inputs:	int y, the starting location
					int x, the other starting coordinate

			outputs: None but it modifies lastY and lastX. 
					 Ironically these are the STARTING positions...
		"""
		
		# if no values are supplied find the opposite of the maze exit... I think
		if y == -1 and x == -1:
			y = abs(self.maxY - self.startY)
			x = abs(self.maxX - self.startX)
		
		# Prepare to meet the neighbors.
		neighbors = {}
		# self__get_neighbor takes coordinates and a flag which determines if 
		# visited neighbors should return. The default is to only return non-visited
		# neighbors
		returnVisited = True

		# I am trying to make sure I don't spawn the player in a wall.
		# this is the fundamental problem with teleportation as a superpower.
		if self.maze[y][x]['wall'] or not self.__in_range__(y,x):
			
			neighbors = self.__get_neighbor__(y,x,returnVisited)
		else:
			self.lastY = y
			self.lastX = x
			return
		try :
			# OMG this is so janky. It fails so often... 
			# It fails because the current version of neighbors only returns non-visited cells...
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
		"""
			This is used to check the contents of a cell in the maze.
			For the most part it works pretty well.
			I do want to move the items out of the main maze structure
			Essentially I need another structure with a tuple of rows/columns
			and the items held therein... We'll see how it goes

			Inputs:	int y: the y coordinate cell to check
					int x: the x coordinate cell to check
					player p: the player who encountered the cell.

			Output:	None but it modifies the player.

		"""
		# see if the player has visited the cell
		# this is used to add score and, eventually, 
		# change the cells that can be viewed
		# I tried using the visited value that was already present
		# but, for whatever reason, it didn't work...
		if not self.maze[y][x]['checked']:
			self.maze[y][x]['checked'] = True
			self.__addScore__(1,p)

		# Check the cell for contents.
		if self.maze[y][x]['contains']:
			for item in self.maze[y][x]['contains']:
				
				# is it an item...
				# this probably needs to change to take advantage of the
				# items class... or maybe not...
				# 
				if item in self.items:
					if self.maze[y][x]['contains'][item]:
						self.items[item]['action'](y,x,p)

				# same as above but for enemies instead of
				# items
				if item in self.enemies:
					self.enemies[item]['encounter'](y,x)

		# Find exit? good!
		self.__found_exit__(y,x)

				

	def __found_exit__(self,y,x):
		"""
			This is also kind of janky.
			Mostly I feel like the whole moveTest thing
			needs to change.

			Inputs:	int y the y coordinate to check for an exit
					int x the x coordinate to check for an exit

			Output:	None... But it modifies self.moveTest
			
		"""
		if y == self.startY and x == self.startX:
			self.moveTest = False

	def __repr__(self):
		"""
			Shows the final maze layout and the score.
		"""
		maze = ''
		checked = 0
		total = 0
		for cols in self.maze:
			for rows in self.maze[cols]:
				if self.maze[cols][rows]['wall'] :
					# print '.',
					maze += self.wall
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


	def __get_neighbor__(self,y,x,vis=False,diagonals=False):
		"""
			This seems to work relatively well.
			Though on occasion it spits out an empty set.
			It returns all the neighbors of a cell. 
			
			inputs:	int y the y coordinate at the center to check
					int x the x coordinate at the center to check
					bool vis: return visited cells
							  default False
					bool diagonals: When true returns diagonal cells
									otherwise it returns n,e,w,s
									default False
		"""
		neighbors = {}
		# check north and northwest cells
		if (y-2) >= self.minY and not self.maze[y-2][x]['visited'] or vis:
			neighbors['N'] = {'y':y-2,'x':x} 
			if diagonals and x-2 >= self.minX:
				neighbors['NW'] = {'y':y-2,'x':x-2}

		# check east and south east
		if (x+2) <= self.maxX-1 and not self.maze[y][x+2]['visited'] or vis:
			neighbors['E'] = {'y':y,'x':x+2}
			if diagonals and (y+2) <= self.maxY:
				neighbors['SE'] = {'y':y+2,'x':x+2} 

		# check the north and nw corners
		if (x-2) >= self.minX and not self.maze[y][x-2]['visited'] or vis:
			neighbors['W'] = {'y':y,'x':x-2}
			if diagonals and (y-2) >= self.minY:
				neighbors['NW'] = {'y':y-2,'x':x-2}

		# check south cell and south west cell
		if (y+2) <= self.maxY-1 and not self.maze[y+2][x]['visited'] or vis:
			neighbors['S'] = {'y':y+2,'x':x}
			# check southwest cell
			if diagonals and x+2 <= self.maxX:
				neighbors['SW'] = {'y':y+2,'x':x+2}
		# print neighbors
		return neighbors

	def __generate_maze__(self,y,x):
		"""
			Alrighty. The meat and potatoes.
			Uses a modified recursive backtrace path finding algorithm
			Also generates random rooms... more details in the function

			inputs:	int y the y coordinate of the cell to check
					int x the x coordinate of the cell to check
					curses object load: used to display the loading screen.
		"""

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
		"""
			This isn't being used...
			It was designed to convert all the cells from visited to not...
		"""
		for col in range(self.maxY):
			for row in range(self.maxX):
				if self.__in_range__(col,row):
					self.maze[col][row]['visited'] = False

	def __setScore__(self, score,p):
		"""
			set the players score. If I ever make this multiplayer...
			This will help add the score to the correct player.

			inputs: int score the score to set
					player p the player whose score will be set

			output:	None but it modifies score
		"""
		p.score = score

	def __addScore__(self,score,p):
		"""
			Adds to the players score. If I ever make this multiplayer...
			This will help add a score to the correct player.

			inputs: int score the score to set
					player p the player whose score will be set

			output:	None but it modifies score
		"""
		p.score = p.score + score

	def __place_items__(self):
		"""
			Randomly assigns items to cell
			Currently only assigns bombs... 
			I'll need to modify it to add cash	
			and food. 
			Eventually I am going to swap it out to use a different icon...
		"""
		
		for x in range(random.choice(range(3,6))):
			
			y = random.choice(range(self.maxY))
			x = random.choice(range(self.maxX))
			while self.maze[y][x]['wall']:
				y = random.choice(range(self.maxY))
				x = random.choice(range(self.maxX))
			
			self.maze[y][x]['contains']['bomb'] = True


	def __make_room__(self,y,x,size=-1):
		"""
			Used to generate random rooms to make the maze more interesting.
			Uses neighbors...

			inputs:	int y the y coordinate of the origin of the room to generate
					int x the x coordinate of the origin of the room to generate
					int size the diameter of the room. Default -1

			output: none but it modifies self.maze
		"""
		
		if self.debug:
			msg = "calling make_room with y=%d,x=%d,size=%d" %(y,x,size)
			self.log._log(msg,"728")
		
		# if no size is specified randomly pick on based on self.maxRoomSize
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
						self.log._err(e,values,"748")


	def __place_bomb__(self,y,x,sbomb,p):
		"""
			Used to allow a player to add a bomb to the map.

			Inputs:	int y the y coordinate where the bomb goes
					int x the x coordinate where the bomb goes
					array sbomb: the array of bombs which have been placed
					player p: the player who placed the bomb.

			output: none but it modifies sbomb

		"""
		if p.inventory['bombs']['quantity'] > 0:
			p.inventory['bombs']['quantity'] -= 1
			sbomb[len(sbomb)+1] = {'counter':items.bombs()['timer'],'y':y,'x':x}

	def __det_bomb(self,bomb,stdscr):
		"""
			Used to detonate bombs...

			inputs:	array bomb: this has the tuple of coordinates
					curses screen object stdscr: allows the animation to be drawn

			Output:	none but it modifies self.maze
		"""
		for col in range(bomb['y']-1,bomb['y']+2):
			for row in range(bomb['x']-2,bomb['x']+3):
				stdscr.addstr(col,row,u"\U00002601".encode("utf-8"))
				if self.__in_range__(col,row):
					self.maze[col][row]['wall'] = False

	def __get_bomb__(self,y,x,p):
		"""
			allows players to pickup bombs.
			If the player isn't over capacity then it adds the bomb
			to their inventory count.

			Inputs: int y the y coordinate to update
					int x the x coordinate to update
					player p: the player to add the bomb too

			output:	none but it modifies the player and self.maze
		"""
		# p.inventory['bombs']['quantity'] += 3
		if p.addItem('bombs',3):
			self.maze[y][x]['contains']['bomb'] = False
			self.__addScore__(self.items['bomb']['score'],p)

	def __in_range__(self,y,x):
		"""
			check if the y and x values are in screen range
			+/- 1 to account for the screen border.
		"""
		return self.minY < y < self.maxY-1 and self.minX < x < self.maxX-1


	def __get_window__(self,size="small"):
		"""
			Used to generate a sub-window.
			I will be using this when I finally get combat to work...
			inputs:	string size generates the size widow based on overall max 
					window size. Current options are: small(default), medium

			output: returns a curses window object
		"""
		if size.lower() == 'small':
			startY = int(self.maxY*.5)
			startX = int(self.maxX*.5)
			endY   = int(self.maxY*.1)
			endX   = int(self.maxX*.1)
			return curses.newwin(startY,startX,endY,endX)
		elif size.lower() == 'medium':
			startY = int(self.maxY*.5)
			startX = int(self.maxX*.5)
			endY   = int(self.maxY*.25)
			endX   = int(self.maxX*.25)
			return curses.newwin(startY,startX,endY,endX)
		else :
			startY = int(self.maxY*.5)
			startX = int(self.maxX*.5)
			endY   = int(self.maxY*.1)
			endX   = int(self.maxX*.1)
			return curses.newwin(self.maxY*.5,self.maxX*.5,self.maxY*.25,self.maxX*.25)
