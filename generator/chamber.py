
from random import randint, random
from .room import Room

# - these are used like C defines, for clarity
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

class Chamber:
	def __init__(self, border, rooms):
		self.border = border
		self.rooms = rooms
		self.check_params()
		self.wall = None
		self.wall_base = None
		self.wall_bias = 8
		self.inner_borders_list = []

	def check_params(self):
		if any(type(edge) != int for edge in self.border):
			raise TypeError('all elements of border must be ints')
		if any(edge < 0 for edge in self.border):
			raise ValueError('all elements of border must be strictly positive')
		if self.border[0] > self.border[1] or self.border[2] > self.border[3]:
			raise ValueError('border: [[UP, DOWN], [LEFT, RIGHT]] with \
				UP < DOWN and LEFT < RIGHT')
		if any(isinstance(room, Room) == False
			for room_row in self.rooms
			for room in room_row):
			raise TypeError('all elements of rooms must be instances of Room')

	def divide(self):
		self.add_wall()
		self.pierce_wall()
		self.inner_chambers()

	def add_wall(self):
		# - if height (DOWN - UP) > width (RIGHT - LEFT) cut horizontally to 
		# generate less narrow rooms
		if ((self.border[DOWN] - self.border[UP])
			> (self.border[RIGHT]- self.border[LEFT])):
			self.wall_base = LEFT
			# - pick a random row as wall position with bias towards center of 
			# distribution to avoid walls near the avoid long narrow rooms
			self.wall = self.boosted_normal(self.border[UP],
				self.border[DOWN] - 2, self.wall_bias)
			# - close the adjacent cells
			for column in range(self.border[LEFT], self.border[RIGHT]):
				self.rooms[self.wall][column].open[DOWN] = False
				self.rooms[self.wall + 1][column].open[UP] = False
		else:
			self.wall_base = UP
			self.wall = self.boosted_normal(self.border[LEFT],
				self.border[RIGHT] - 2, self.wall_bias)
			for row in range(self.border[UP], self.border[DOWN]):
				self.rooms[row][self.wall].open[RIGHT] = False
				self.rooms[row][self.wall + 1].open[LEFT] = False

	def boosted_normal(self, low, high, bias):
		# returns a random int between low and high, with a bias towards the
		# middle of the range
		distribution = [randint(low, high) for i in range(bias)]
		return int(sum(distribution) / bias)

	def pierce_wall(self):
		# - pick a random location in the wall
		# - open the adjacent cells
		if self.wall_base == LEFT:
			hole = randint(self.border[LEFT], self.border[RIGHT] - 1)
			self.rooms[self.wall][hole].open[DOWN] = True
			self.rooms[self.wall + 1][hole].open[UP] = True
		else:
			hole = randint(self.border[UP], self.border[DOWN] - 1)
			self.rooms[hole][self.wall].open[RIGHT] = True
			self.rooms[hole][self.wall + 1].open[LEFT] = True

	def inner_chambers(self):
		# - if the wall is more than one row away from a given border
		# - create an inner border from the current border with the wall 
		# as a new edge
		# - add that inner border to the list
		self.inner_borders_list = []
		if self.wall_base == LEFT:
			if self.wall > self.border[UP]:
				inner_border = self.border[:]
				inner_border[DOWN] = self.wall + 1
				self.inner_borders_list.append(inner_border)
			if self.wall < self.border[DOWN] - 2:
				inner_border = self.border[:]
				inner_border[UP] = self.wall + 1
				self.inner_borders_list.append(inner_border)
		else:
			if self.wall > self.border[LEFT]:
				inner_border = self.border[:]
				inner_border[RIGHT] = self.wall + 1
				self.inner_borders_list.append(inner_border)
			if self.wall < self.border[RIGHT] - 2:
				inner_border = self.border[:]
				inner_border[LEFT] = self.wall + 1
				self.inner_borders_list.append(inner_border)
