
import argparse
from generator.maze import Maze
from solver.solver import Solver
from display.display import Printer

def labyrinth(args):
	# create maze, set it with rows and columns option
	maze = Maze(args.rows, args.columns)
	# create printer and set it with print option
	printer = Printer(maze, pause = args.pause)
	maze.set_maze()
	# print according to display options
	if args.display == 'both' or args.display == 'without-solution':
		printer.print_maze()
	if args.no_solve == False:
		# create solver and set it with maze object
		solver = Solver(maze)
		solver.solve()
		# print according to display options
		if args.display == 'both' or args.display == 'with-solution':
			printer.print_maze()
			print('Shortest path:', ', '.join(map(str, solver.shortest)))
		return solver.shortest

parser = argparse.ArgumentParser()
parser.add_argument('--rows',
	help = 'number of rows in the maze',
	type = int,
	default = 40)
parser.add_argument('--columns',
	help = 'number of columns in the maze',
	type = int,
	default = 30)
parser.add_argument('--no-solve',
	help = 'do not solve',
	action = 'store_true')
parser.add_argument('--display',
	choices = ['none', 'without-solution', 'with-solution', 'both'],
	default = 'with-solution',
	help = 'specifies what to print')
parser.add_argument('--pause',
	help = 'pause after printing',
	action = 'store_true')
args = parser.parse_args()

if ((args.display == 'both' or args.display == 'with-solution')
	and args.no_solve):
	print('Conflicting arguments: display with-solution and no-solve')
	exit()
else:
	labyrinth(args)
