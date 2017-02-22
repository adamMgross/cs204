"""CS2204 Homework#3: Maze generation and path finding

Name:
VUnetID:
Email:
"""

class Cell:
    """
    Cell objects represent a single maze location with up-to 4 walls.

    The .N, .E, .S, .W attributes represent the walls in the North,
    East, South and West directions. If the attribute is True, there is a
    wall in the given direction.

    The .x and .y attributes store the coordinates of the cell.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.N = True
        self.E = True
        self.S = True
        self.W = True
        self.walls = [self.N, self.E, self.S, self.W]
        self.visited = False

    def remove_wall(self, direction):
        """
        Remove one wall - keep all neighbors consistent
        Direction is one of these strings: 'N', 'E', 'S', 'W'
        """
        direction = direction.upper()

        loc = ' @(x=%d, y=%d)' % (self.x, self.y)
        if direction == 'W':
            if self.x < 1:
                raise ValueError('cannot remove side wall on west' + loc)
            if self.W:
                self.W = False
                assert maze[self.x - 1][self.y].E
                maze[self.x - 1][self.y].E = False
        if direction == 'E':
            if self.x >= size_x - 1:
                raise ValueError('cannot remove side wall on east' + loc)
            if self.E:
                self.E = False
                assert maze[self.x + 1][self.y].W
                maze[self.x + 1][self.y].W = False
        if direction == 'N':
            if self.y < 1:
                raise ValueError('cannot remove side wall on north' + loc)
            if self.N:
                self.N = False
                assert maze[self.x][self.y - 1].S
                maze[self.x][self.y - 1].S = False
        if direction == 'S':
            if self.y >= size_y - 1:
                raise ValueError('cannot remove side wall on south' + loc)
            if self.S:
                self.S = False
                assert maze[self.x][self.y + 1].N
                maze[self.x][self.y + 1].N = False

    def has_wall(self, direction):
        """
        True if there is a wall in the given direction
        Direction is one of these strings: 'N', 'E', 'S', 'W'
        """
        return getattr(self, direction.upper())
    def __repr__(self):
        s = ''
        if self.W:
            s += '|'
        if self.S:
            s += '_'
        if self.E:
            s += '|'
        return s


# Global variables for the maze and its size
size_x = size_y = 32
maze = [[Cell(x, y) for y in range(size_y)] for x in range(size_x)]

def build_maze():
    """
    Build a valid maze by tearing down walls

    The function has access to the following global variables:
        size_x - integer, the horizontal size of the maze
        size_y - integer, the vertical size of the maze
        maze - a two dimensional array (list of lists) for all cells
            e.g. maze[3][4] is a Cell object for x=3, y=4

    This function does not need to return any value but should modify the
    cells (walls) to create a perfect maze.
    When the function is invoked all cells have all their four walls standing.
    """
    global maze
    wall_list = []
    import random

    rand_x = random.randint(0, len(maze[0]) - 1)
    rand_y = random.randint(0, len(maze) - 1)
    rand_cell = maze[rand_y][rand_x]
    rand_cell.visited = True
    
    def append_wall_neighbors(cell, lst):
        
        if cell.W:
            lst.append((rand_cell.x, rand_cell.y, 'W'))
        if cell.N:
            lst.append((rand_cell.x, rand_cell.y, 'N'))
        if cell.E:
            lst.append((rand_cell.x, rand_cell.y, 'E'))
        if cell.S:
            lst.append((rand_cell.x, rand_cell.y, 'S'))
    
    wall_list = []
    append_wall_neighbors(rand_cell, wall_list)
    while wall_list:
        print(wall_list)
        rand_index = random.randint(0, len(wall_list) - 1)
        x, y, direction = wall_list.pop(rand_index)
        delta = (1 if direction == 'E' else -1 if direction == 'W' else 0,
                 1 if direction == 'N' else -1 if direction == 'S' else 0)
        neighbor = maze[(y + delta[1]) % size_y][(x + delta[0]) % size_x]
        if not neighbor.visited:
            try:
                maze[y][x].remove_wall(direction)
            except:
                pass
            neighbor.visited = True
            append_wall_neighbors(neighbor, wall_list)

def find_path(start, end):
    """
    Find a path from the start position to the end

    The start and end parameters are coordinate pairs (tuples) for the
    start and end (target) position. E.g. (0, 0) or (7, 13).

    The function has access to the following global variables:
        size_x - integer, the horizontal size of the maze
        size_y - integer, the vertical size of the maze
        maze - a two dimensional array (list of lists) for all cells
            e.g. maze[3][4] is a Cell object for x=3, y=4

    The function is invoked after build_maze removed the walls to create a
    perfect maze.

    This function shall return a list of coordinate pairs (tuples or lists)
    which list the cell coordinates on a valid path from start to end.
    E.g.: [(0, 0), (0, 1), (1, 1), (2, 1), (3, 1), ..., (7, 13)]
    """
    pass


###############################################################################
# Testing and visualizing results - no need to understand and/or change

def main():
    import sys
    import tkinter

    sys.setrecursionlimit(4096)

    start, end = (0, 0), (size_x - 1, size_y - 1)

    build_maze()
    path = find_path(start, end)

    # checking maze
    n_edges = 0
    for x in range(size_x):
        for y in range(size_y):
            n_node_edges = 0
            for direction in 'NESW':
                n_node_edges += not maze[x][y].has_wall(direction)
            if n_node_edges < 1:
                print('WARNING: walled in cell @ (x=%d, y=%d)' % (x, y))
            n_edges += n_node_edges
    n_perfect_edges = (size_x * size_y - 1) * 2
    if n_edges < n_perfect_edges:
        print('WARNING: not a perfect maze, too many walls')
    if n_edges > n_perfect_edges:
        print('WARNING: not a perfect maze, redundant paths')

    # checking path
    try:
        assert len(path) >= 2
        if path[0] != start:
            print('WARNING: invalid starting point for path', path[0])
        if path[-1] != end:
            print('WARNING: invalid endpoint for path', path[-1])

        prev = None
        for step in path:
            assert 0 <= step[0] < size_x
            assert 0 <= step[1] < size_y
            if prev is not None:
                dst = abs(step[0] - prev[0]) + abs(step[1] - prev[1])
                if dst != 1:
                    print('WARNING: invalid step in path', prev, step)
                prev = step

    except Exception as e:
        print('Ignoring invalid path object:', path, e)
        path = None

    cell_size = 20
    master = tkinter.Tk()
    canvas = tkinter.Canvas(master, width=size_x * cell_size + 1,
                            height=size_y * cell_size + 1,
                            bd=0, highlightthickness=0, relief='ridge')
    canvas.pack()
    for x in range(size_x):
        for y in range(size_y):
            if maze[x][y].N:
                canvas.create_line(cell_size * x, cell_size * y,
                                   cell_size * (x + 1), cell_size * y)
            if maze[x][y].E:
                canvas.create_line(cell_size * (x + 1), cell_size * y,
                                   cell_size * (x + 1), cell_size * (y + 1))
            if maze[x][y].S:
                canvas.create_line(cell_size * x, cell_size * (y + 1),
                                   cell_size * (x + 1), cell_size * (y + 1))
            if maze[x][y].W:
                canvas.create_line(cell_size * x, cell_size * y,
                                   cell_size * x, cell_size * (y + 1))

    if path:
        line = [x * cell_size + cell_size // 2 for step in path for x in step]
        canvas.create_line(*line, fill='red', width=2)

    radius = cell_size // 3
    img_start = [cell_size * x + cell_size // 2 for x in start]
    canvas.create_oval(img_start[0] - radius,
                       img_start[1] - radius,
                       img_start[0] + radius,
                       img_start[1] + radius, fill='red')
    img_end = [cell_size * x + cell_size // 2 for x in end]
    canvas.create_oval(img_end[0] - radius,
                       img_end[1] - radius,
                       img_end[0] + radius,
                       img_end[1] + radius, fill='green')

    master.title('Maze')
    master.lift()
    master.call('wm', 'attributes', '.', '-topmost', True)
    tkinter.mainloop()

if __name__ == '__main__':
    main()
