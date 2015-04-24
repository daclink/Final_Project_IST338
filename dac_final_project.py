#
# FinalProject.py
#
# Name:Drew A. Clinkenbeard
# Random Maze
#	http://en.wikipedia.org/wiki/Maze_generation_algorithm
#
# curses coordinates go y,x
# 0,0 is the top left corner.



import sys
import random
import time
import curses
import locale
import random
import math

# sys.setrecursionlimit(10000)

class ist338_the_game():

	def __init__(self, debug=True):
		
		locale.setlocale(locale.LC_ALL, '')
		code = locale.getpreferredencoding()
		self.debug = debug
		if debug :
			print "Hello there! deubg is ", debug
		# Setup Player
		self.setScore(0)
		
		# Setup Screen
		stdscr = curses.initscr()
		curses.savetty() #make sure we can put the screen back the way we found it
		curses.noecho() #prevent keypresses appearing on screen
		curses.cbreak() #interpret input with out return
		stdscr.keypad(1) #everyone loves the keypad
		stdscr.clearok(1) #allow the screen to be cleared
		curses.curs_set(0) #hide the caret

		self.minX = minX	= 0
		#how far to the right we can go.
		#Leaving room for messages.
		self.maxX = maxX	= stdscr.getmaxyx()[1] -15

		self.minY = minY	= 0
		##how far down we can go
		#leaving room for messages
		self.maxY = maxY	= stdscr.getmaxyx()[0] -5

		self.maze = {}
		self.minY = self.minX = 0
		self.visited = 0
		for row in range(maxY):
			self.maze[row] = {}
			for col in range(maxX):
				self.maze[row][col] = {}
				self.maze[row][col]["visited"] = False
				self.maze[row][col]["contains"] = {}
				self.visited += 1
				self.maze[row][col]["wall"] = True

		self.__get_start__()
		self.__generate_maze__(self.startY,self.startX)
		stdscr.clear()
		stdscr.refresh()
		# print self.maze

		
		# item = "0"
		# for y in range(maxY):
		# 	for x in range(maxX):
		# 		stdscr.addstr(y,x,item.encode("utf-8"))
		# 		stdscr.refresh()
		# 		time.sleep(0.001)
		# 		# stdscr.clear()

		moveTest = True
		charPos = {'y':0,'x':0}
		while moveTest:
			move = stdscr.getch()
			if move == 113 : 
				moveTest = False
			elif move == curses.KEY_RIGHT:
				charPos['x'] += 1
			elif move == curses.KEY_LEFT:
				charPos['x'] -= 1
			elif move == curses.KEY_UP:
				charPos['y'] -= 1
			elif move == curses.KEY_DOWN:
				charPos['y'] += 1 
			stdscr.clear()
			stdscr.addstr(charPos['y'],charPos['x']-1,item.encode("utf-8"))
			stdscr.refresh()


		time.sleep(1)
		##put it all back
		curses.resetty()
		curses.endwin()
		



		return None

	def __repr__(self):
		
		# for row in self.maze:
		# 	for col in self.maze[row]:
		# 		print u"\U0001f355",
		# 	print ""
		# s = "Final Score = %d" %self.score

		# print "Max X = %d Max Y = % d" %(self.maxX, self.maxY)
		# self.face = face = u"\U0001f47e"
		# xpos = int(math.ceil(maxX/2))
		# ypos = int(math.ceil(maxY/2))
		# return s
		maze = ''
		for cols in self.maze:
			for rows in self.maze[cols]:
				if self.maze[cols][rows]['wall'] :
					# print '.',
					maze += '#'
				else:
					# print ' ',
					maze += '_'
			# print '\n'
			maze += '\n'

		return maze


	def testScreen(self, stdscr,x,y,item):
		stdscr.addstr(y,x,item.encode("utf-8"))
		stdscr.refresh()
		time.sleep(.1)

	def setScore(self, score):
		self.score = score

	def __get_start__(self):
		self.startY = random.choice(self.maze.keys())
		self.startX = random.choice(self.maze[self.startY].keys())

	def __get_neighbor__(self,y,x):
		neighbors = {}
		if (y-2) >= self.minY:
			neighbors['N'] = {'y':y-2,'x':x}
		if (x+2) <= self.maxX:
			neighbors['E'] = {'y':y,'x':x+2}
		if (x-2) >= self.minX:
			neighbors['W'] = {'y':y,'x':x-2}
		if (y+2) <= self.maxY:
			neighbors['S'] = {'y':y+2,'x':x}
		# print neighbors
		return neighbors

	def __generate_maze__(self,y,x):
		
		self.maze[y][x]['wall']= False
		self.maze[y][x]['visited'] = True
		self.visited -= 1
		neighbors = self.__get_neighbor__(y,x)

		while neighbors:
			rand_neighbor = random.choice(neighbors.keys())
			# print rand_neighbor
			
			ny = neighbors[rand_neighbor]['y']
			nx = neighbors[rand_neighbor]['x']

			if not self.maze[ny][nx]['visited']:
				# self.visited -= 1

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
			
			if self.visited > 0:
				self.__generate_maze__(ny,nx)

		return 0



	




foo = ist338_the_game()

# print foo


# class rw2D():
	
# 	def __init__(self, debug=False):
# 		locale.setlocale(locale.LC_ALL, '')
# 		code = locale.getpreferredencoding()
# 		##start curses
# 		stdscr = curses.initscr()
# 		curses.noecho() #prevent keypresses appearing on screen
# 		curses.cbreak() #interpret input with out return
# 		stdscr.keypad(1) #everyone loves the keypad
# 		stdscr.clearok(1) #allow the screen to be cleared
# 		curses.curs_set(0) #hide the caret

# 		self.minX = minX	= 0
# 		#how far to the right we can go.
# 		#Leaving room for messages.
# 		self.maxX = maxX	= stdscr.getmaxyx()[1] -10

# 		self.minY = minY	= 0
# 		##how far down we can go
# 		#leaving room for messages
# 		self.maxY = maxY	= stdscr.getmaxyx()[0] -5

# 		#initializing the stepcounter
# 		step_counter  = 0

		
# 		self.face = face = u"\U0001f47e"
# 		xpos = int(math.ceil(maxX/2))
# 		ypos = int(math.ceil(maxY/2))
		
# 		self.SO 	= SO 	= self.__rand_local() + [u"\U0001f47d", self.gf,	False,  3]
# 		self.grades	= grade = self.__rand_local() + [u"\U0001f393", self.gts,	False,	0]
# 		self.score	= score = self.__rand_local() + [u"\U0001f4af", self.oh,	False,	1]
# 		self.Food   = food 	= self.__rand_local() + [u"\U0001f355", self.dorm,	False,	2]

# 		items = [grade,score,food]
		

# 		house  = u"\U0001f3e0"
# 		school	= u"\U0001f3eb"
# 		prof 	= u"\U0001f645"
# 		lh		= u"\U0001F3E9"
# 		foo =""


# 		while 1:
			
# 			stdscr.addstr(minY,minX, house.encode("utf-8"))
# 			stdscr.addstr(maxY,maxX, school.encode("utf-8"))
# 			stdscr.addstr(minY,maxX, lh.encode("utf-8"))
# 			stdscr.addstr(maxY,minX, prof.encode("utf-8"))
# 			Steps = "Steps taken : "+ str(step_counter)
# 			stdscr.addstr(maxY+1,minX, Steps)
# 			stdscr.refresh()

# 			#main char movment
# 			xpos = xpos + self.__rand_step()
# 			ypos = ypos + self.__rand_step()
# 			if xpos <= minX : xpos = minX
# 			if xpos >= maxX : xpos = maxX
# 			if ypos <= minY : ypos = minY
# 			if ypos >= maxY : ypos = maxY
# 			if debug : foo = "[y" +str(ypos) +",x" + str(xpos)+"]"
# 			stdscr.addstr(ypos,xpos, face.encode("utf-8")+foo)

			
			
# 			if  SO[4] == False :
# 				#gf movement 
# 				SO[0] = SO[0] + self.__rand_step()
# 				SO[1] = SO[1] + self.__rand_step()
# 				SO[4] = self.__hit_map(SO,[ypos,xpos]) 

# 			else :
# 				# stdscr.addstr(minY,maxX-2, str(SO[4]))
# 				l = SO[3]()
# 				ypos = ypos + l[0]
# 				xpos = xpos + l[1]
# 				SO[0] = ypos
# 				SO[1] = (xpos + 1)

# 			if SO[1] < minX : SO[1] = minX
# 			if SO[1] > maxX : SO[1] = maxX
# 			if SO[0] < minY : SO[0] = minY
# 			if SO[0] > maxY : SO[0] = maxY
			
# 			stdscr.addstr(SO[0],SO[1],SO[2].encode("utf-8")+foo)
# 			# stdscr.addstr(minY,maxX+1,"GF Stats")
# 			# gfPos = "y:%d,x:%d" %(SO[0],SO[1])
# 			# stdscr.addstr(minY+2,maxX+1, gfPos)
# 			# stdscr.addstr(minY+3,maxX+1, "fnd"+str(SO[4]))	
# 			stdscr.refresh()
# 			# time.sleep(.1)

# 			for x in items:
# 				stdscr.addstr(x[0],x[1],x[2].encode("utf-8"))

# 			if debug and step_counter == 5:
# 				xpos = items[1][1]
# 				ypos = items[1][0]

# 			for x in items:
# 				if self.__hit_map(x,[ypos,xpos]):
# 					x[4] = True
# 					x[0] = maxY+2
# 					x[1] = minX+(x[5]*2)
# 					blah = x[5]
# 					items[blah] = x
				

# 			for x in items:
# 				if x[4] == True:
# 					temp = x[3]()
# 					ypos = ypos + temp[0]
# 					xpos = xpos + temp[1]
# 					items[x[5]][0]=maxY+2
# 					items[x[5]][1]=minX+x[5]
			
# 			stdscr.refresh()


# 			## HOME
# 			if xpos <= minX and ypos<=minY :
# 				MSG = " made it home! "
# 				self.end(stdscr,MSG,house)
# 				break
# 			## Prof
# 			if xpos <= minX and ypos>=maxY : 
# 				MSG = " Went to see the professor! "
# 				self.end(stdscr,MSG,prof)
# 				break
# 			## LH
# 			if xpos >= maxX and ypos <= minY : 

# 				MSG = " a necessary break..."
# 				self.end(stdscr,MSG,lh)
# 				break
# 			## School
# 			if xpos >= maxX and ypos >= maxY : 
# 				MSG = " made it to school! "
# 				self.end(stdscr,MSG,school)
# 				break

			
# 			stdscr.refresh()
# 			time.sleep(.1)
# 			if debug : time.sleep(.1)
# 			stdscr.clear()
# 			step_counter +=1
		
# 		stdscr.addstr(minY+1,minX, Steps)
# 		stdscr.addstr(minY+2,minX, "press any key to continue")
# 		curses.curs_set(1)
# 		stdscr.getch()
		
# 		curses.curs_set(1)
# 		##put it all back
# 		curses.curs_set(1)
# 		curses.nocbreak()
# 		stdscr.keypad(0)
# 		curses.echo()
# 		curses.endwin()
# 		return None

# 	def end(self,stdscr,MSG,icon):

# 			stdscr.clear()
# 			stdscr.addstr(self.minY,self.minX, self.face.encode("utf-8"))
# 			stdscr.addstr(self.minY,self.minX+2, MSG.encode("utf-8"))
# 			msgLen = 2+self.minX+len(MSG)
# 			stdscr.addstr(self.minY,msgLen, icon.encode("utf-8"))
# 	def gf(self):
# 		"""
# 			the lovely SO... hmmm time for a break.
# 			bias our hero toward the love hotel.
# 		"""
# 		return [-2,1]

# 	def gts(self):
# 		"""
# 		GO to School!
# 		Bias our hero toward school.
# 		"""
# 		return [2,1]
		
# 	def oh(self):
# 		"""
# 		Office hours. Gotta get those grades!
# 		bias our hero toward the prof
# 		"""
# 		return [+2,-1]
# 	def dorm(self):
# 		"""delicious pizza!
# 			ahh yes. Food. Lets get more.
# 			bias our hero toward the dorms.
# 		"""
# 		return [-3,-2]

# 	def __rand_local(self):
# 		"""Get a random location
# 		"""
# 		return [random.choice(range(self.minY+4,self.maxY-10)),
# 			    random.choice(range(self.minX+4,self.maxX-10))]
# 	def __rand_step(self):
# 		"""
# 			Generate a random step
# 		"""
# 		return random.choice([-1,1])

# 	def __hit_map(self, x, player):
# 		"""Calclulate a hit...
# 		"""
# 		for y in range(-1,2) :
# 			if (x[0]+y) == player[0]:
# 				for z in range(-1,2):
# 					if (x[1]+z) == player[1] :
# 						return True
# 		return False
# 	def __debug(self,msg,stdscr):
# 		stdscr.addstr(self.maxY+2,self.minX, msg)
# 		stdscr.refresh()
# 		time.sleep(.1)



