import random
import sys

sys.setrecursionlimit(100000)
class mm():
	
	def __init__(self, y=15,x=15):
		maze = {}
		self.maxY = y-1
		self.maxX = x-1
		self.minY = self.minX = 0
		self.visited = 0
		item =	u"\U0001f355"

		for cols in range(y):
			maze[cols] = {}
			for rows in range(x):
				maze[cols][rows] = {}
				maze[cols][rows]['visited'] = False
				self.visited += 1
				maze[cols][rows]['wall'] = True

		self.maze = maze
		self.__get_start__()
		self.__generate_maze__(self.startY,self.startX)

	def __get_start__(self):
		self.startY = random.choice(self.maze.keys())
		self.startX = random.choice(self.maze[self.startY].keys())

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

# maze = maze_maker()

# print maze.maze

# maze

