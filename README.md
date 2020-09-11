# maze
A maze generator, a maze solver, and a display for both.
You need a terminal that supports raw ansi escape codes.

# usage
usage: labyrinth.py [-h] [--rows ROWS] [--columns COLUMNS] [--no-solve]
                    [--display {none,without-solution,with-solution,both}]
                    [--pause]

optional arguments:
  -h, --help            show this help message and exit
  --rows ROWS           number of rows in the maze
  --columns COLUMNS     number of columns in the maze
  --no-solve            do not solve
  --display {none,without-solution,with-solution,both}
                        specifies what to print
  --pause               pause after printing

# generator
recursive division algorithm:
1 - start with the maze borders as list of chambers coords (1 element)
2 - pop and process first element of chambers list
3 - add wall at random location in chamber
4 - pierce hole in the wall
5 - create an inner chamber for each border if abs(border - wall) > 1
6 - prepend new chambers to list
7 - repeat until the list is empty

Reason for choice : I looked up maze generation algorithms, and used the info 
from this site : http://people.cs.ksu.edu/~ashley78/wiki.ashleycoleman.me/index.php/Recursive_Division.html
to make my choice.
The recursive division is simple and has no bias, and works well with the
rectangular grid from the subject.

# solver
Breadth First Search (BFS):
1 - with parent list = start location, parent distance = 0
2 - the children are the unvisited rooms accessible from the parent list rooms
3 - set children's distance to parent distance + 1
4 - set each children's to the cell from the parent list that you reached it
from
5 - parent list = children list
6 - repeat 2 to 4 until end location is included in children
7 - from end, follow the parent chain until you find start

Reason for choice : if there is a path, the BFS is guaranteed to find it, it
works as well as Dijkstra considering there are no weights to consider (all 
rooms have an equal distance between them), and it provides the shortest path
upon completion.
I also know this algorithm really well from a previous project.
