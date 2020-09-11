
from generator.room import Room
from generator.maze import Maze

# I use these as I would use defines in C, for clarity
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

SINGLE_V = u'\u2502'
PREFIX = '\033[1'
COLOR_START = ';94'
COLOR_END = ';92'
UNDERLINE = ';4'
SUFFIX = '\033[0m'

symbol_dict = {
	'shortest': u'\u25A0',
	'start': 'S',
	'end': 'E',
	'default': u'\u2022',
}

class Printer:
	def __init__(self, maze, pause = False):
		self.maze = maze
		self.pause = pause
		self.check_params()
	
	def check_params(self):
		if isinstance(self.maze, Maze) == False:
			raise TypeError('maze must be instance of Maze class')

	def print_room_info(self, room):
		print("ROOM: status: %s, coord: %s, open: %s, neighbors: %s, distance: %s"
			% (room.status, room.coord, room.open, room.neighbors, room.distance))

	def print_room(self, room):
		room_prefix = PREFIX
		# get symbol
		symbol = symbol_dict[room.status]
		# add color
		if room.status == 'start':
			room_prefix += COLOR_START
		elif room.status == 'end' or room.status == 'shortest':
			room_prefix += COLOR_END
		# add DOWN and RIGHT borders
		if room.open[DOWN] == False:
			room_prefix += UNDERLINE
		if room.open[RIGHT] == False:
			symbol += SUFFIX + SINGLE_V
		else:
			symbol += ' ' + SUFFIX
		return room_prefix + 'm' + symbol

	def print_maze(self):
		display = " " + (PREFIX + 'm_' + SUFFIX) * 2 * self.maze.column_max \
			+ '\n'
		# check in case the class instance was set with an empty maze
		if self.maze.rooms == None:
			raise ValueError('maze must not be empty')
		for row in self.maze.rooms:
			display += SINGLE_V + " "
			for room in row:
				display += self.print_room(room)
			display += " \n"
		print(display)
		if self.pause:
			input("Press Enter to continue...")
