
from random import randrange, random
from .room import Room
from .chamber import Chamber

# I use these as I would use defines in C, for clarity
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


class Maze:
	''' Generate a square maze using the recursive divider algorithm.
	The maze is a grid rows * columns of rooms.
	The rooms consist of :
	 - a 'neighbors' attribute listing the room's neighbors on the grid; 
	 - an 'open' attribute stocking the state of neighbors;
	 - a distance to start (used for solving);
	 - one of the 'None', 'start', 'end' or 'shortest' status (mainly useful 
	 for clearer representation).
	 '''
	def __init__(self, rows = 40, columns = 30):
		if type(rows) != int or type(columns) != int:
			raise TypeError("rows and columns must both be ints")
		elif not 1 < rows < 1000000 or not 1 < columns < 1000000:
			raise ValueError("rows and columns must be between 2 and 1000000")
		self.row_max = rows
		self.column_max = columns
		self.rooms = [[Room(0, 0) for columns in range(columns)] for row in range(rows)]
		self.start = None
		self.end = None
		self.chambers_list = [[0, rows, 0, columns]]
		self.check_params()
	
	def check_params(self):
		if type(self.row_max) != int or type(self.column_max) != int:
			raise TypeError('rows and columns must be ints')
		if self.row_max < 0 or self.column_max < 0:
			raise ValueError('rows and columns must be strictly positive')

	def set_maze(self):
		self.set_rooms()
		self.set_chamber()
	
	def set_rooms(self):
		self.set_rooms_neighbors()
		self.set_rooms_open()
		self.set_start_end()

	def set_rooms_open(self):
		# close maze borders and pick start and end
		for room in self.rooms[0]:
			room.open[UP] = False
		for row in self.rooms:
			row[0].open[LEFT] = False
			row[self.column_max - 1].open[RIGHT] = False
		for room in self.rooms[self.row_max - 1]:
			room.open[DOWN] = False

	def set_rooms_neighbors(self):
		# set each room's neighbors
		for row in range(self.row_max):
			for column in range(self.column_max):
				room = self.rooms[row][column]
				room.coord = [row, column]
				if row > 0:
					room.neighbors[UP] = self.rooms[row - 1][column]
				if row < self.row_max - 1:
					room.neighbors[DOWN] = self.rooms[row + 1][column]
				if column > 0:
					room.neighbors[LEFT] = self.rooms[row][column - 1]
				if column < self.column_max - 1:
					room.neighbors[RIGHT] = self.rooms[row][column + 1]

	def set_start_end(self):
		# pick side with random, pick location with randrange
		roll = random()
		if roll < 0.25:
			coord = [0, randrange(self.column_max)]
		elif roll < 0.50:
			coord = [self.row_max - 1, randrange(self.column_max)]
		elif roll < 0.75:
			coord = [randrange(self.row_max), 0]
		else:
			coord = [randrange(self.row_max), self.column_max - 1]
		# assign start status to the chosen room
		self.start = self.rooms[coord[0]][coord[1]]
		self.start.status = 'start'
		# assign start status to the chosen room
		coord_end = [self.row_max - coord[0] - 1,
			self.column_max - coord[1] - 1]
		self.end = self.rooms[coord_end[0]][coord_end[1]]
		self.end.status = 'end'

	def set_chamber(self):
		# while there are chambers to process
		while len(self.chambers_list) > 0:
			# pop first chamber from the list
			current_chamber = self.chambers_list.pop(0)
			# process it
			new_chamber = Chamber(current_chamber, self.rooms)
			new_chamber.divide()
			# add new inner chambers to start of the list
			self.chambers_list = new_chamber.inner_borders_list \
				 + self.chambers_list
