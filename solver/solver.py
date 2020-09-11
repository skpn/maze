
from generator.maze import Maze
from generator.room import Room

class Solver:
	''' Finds the shortest path from room 'start' to room 'end' in a Maze class 
	instance via a Breadth First Search
	''' 
	def __init__(self, maze):
		self.maze = maze
		self.shortest = []
		self.frontier = [maze.start]
		self.check_params()
	
	def check_params(self):
		if isinstance(self.maze, Maze) == False:
			raise TypeError('maze must be instance of Maze class')

	def solve(self):
		# check in case the class instance was set with an unset maze
		if self.maze.start == None or self.maze.end == None:
			raise ValueError('maze must be set')
		# distances will be relative to start
		# - set initial distance to 0
		self.maze.start.distance = 0
		# frontier is the group of explored rooms farthest from start
		# - continue until frontier reaches room 'end'
		while not self.maze.end in self.frontier:
			self.expand_frontier()
		# - backtrack to build shortest path list
		self.get_shortest()
		return self.shortest, len(self.shortest)

	def expand_frontier(self):
		children = []
		for room in self.frontier:
			# - get next frontier group
			self.get_children(children, room)
		self.frontier = children

	def get_children(self, children, room):
		for pos in range(4):
			# - include unvisited rooms touching an open side of a frontier room
			if room.open[pos] == True:
				neighbor = room.neighbors[pos]
				# - we set distance when visiting a room -> distance == None
				# means the room is unvisited
				if neighbor.distance == None:
					children.append(neighbor)
					neighbor.distance = room.distance + 1
					neighbor.parent = room

	def get_shortest(self):
		room = self.maze.end
		# - the parent room is the first to have reached the room -> it is on 
		# the shortest path
		while room.parent != self.maze.start:
			self.shortest.insert(0, room.parent.coord)
			room.parent.status = 'shortest'
			room = room.parent
