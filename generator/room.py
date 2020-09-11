
class Room:
	''' A room object to be used by the Maze and Solver classes '''
	def __init__(self, row, column):
		self.coord = [row, column]
		self.neighbors = [None] * 4
		self.open = [True] * 4
		self.status = 'default'
		self.distance = None
		self.parent = None
		self.check_params()
	
	def check_params(self):
		if type(self.coord[0]) != int or type(self.coord[1]) != int:
			raise TypeError('row and column must be ints')
		if self.coord[0] < 0 or self.coord[1] < 0:
			raise ValueError('row and column must be strictly positive')
