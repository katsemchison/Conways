import tkinter as tk
import time
import random

# Rules:
# 1 Any live cell with fewer than 2 live neighbours dies
# 2 Any live cell with 2 or 3 live neighbours lives until the next gen
# 3 Any live cell with more than 3 neighbours dies
# 4 Any dead cell with exactly 3 live neighbours becomes a live cell

# Set constant variables
height, width = 200, 200
square_size = 4
grid_size = 100


def create_grid():
    # create a new array filled with 0's to modify later and return it.
    new_grid = []
    grid_line = []
    for x in range(grid_size):
        grid_line.append(0)
    for y in range(grid_size):
        new_grid.append(list(grid_line))
    return new_grid


def check_if_alive(x, y, g):

    # check if the current cell is up against the walls
    if x > 0:
        # check the above cell
        up = g[x-1][y]
    else:
        up = 0

    if x < grid_size:
        # check the cell below
        down = g[x+1][y]
    else:
        down = 0

    if y < grid_size:
        # check the cell to the right
        right = g[x][y+1]
        if 0 < x < grid_size-1:
            # if it's within the grid, check the upper and lower right
            upper_right = g[x-1][y+1]
            lower_right = g[x+1][y+1]
        elif x < 1:
            # otherwise check if it's in a corner and set the upper and lower right
            upper_right = 0
            lower_right = g[x+1][y+1]
        elif x > grid_size-2:
            upper_right = g[x-1][y+1]
            lower_right = 0
    else:
        right = 0
        upper_right = 0
        lower_right = 0

    if y > 0:
        left = g[x][y-1]
        if 0 < x < grid_size-1:
            upper_left = g[x-1][y-1]
            lower_left = g[x+1][y-1]
        elif x < 1:
            upper_left = 0
            lower_left = g[x+1][y-1]
        elif x > grid_size-2:
            upper_left = g[x-1][y-1]
            lower_left = 0
    else:
        left = 0
        upper_left = 0
        lower_left = 0

    # adding all of the results of the above together allows us to find out if the cell lives or dies.
    # I have left these as possibly never getting assignment because I'd like an error to be raised if there's an issue
    result = up + down + left + right + upper_left + upper_right + lower_left + lower_right

    # 1 Any live cell with fewer than 2 live neighbours dies
    if result < 2:
        return 0
    # 3 Any live cell with more than 3 neighbours dies
    elif result > 3:
        return 0

    # 2 Any live cell with 2 or 3 live neighbours lives until the next gen
    elif result in [2, 3] and g[x][y] == 1:
        return 1
    # 4 Any dead cell with exactly 3 live neighbours becomes a live cell
    elif result == 3 and g[x][y] == 0:
        return 1
    elif result == 2 and g[x][y] == 0:
        return 0


def iterate(g):
    # a new grid has to be created because if we update the old grid, it affects the results of future cell checks.
    temp_grid = create_grid()
    for i in range(0, grid_size-1):
        for j in range(0, grid_size-1):
            temp_grid[i][j] = check_if_alive(i, j, g)
    return temp_grid


def print_grid(g):
    # this was created for testing before I created the GUI, to make sure everything was working fine
    for line in g:
        print(line)


# create the grid and then add a one or a zero randomly to every cell
grid = create_grid()
for row in range(0, grid_size-1):
    for column in range(0, grid_size-1):
        grid[row][column] = random.randint(0, 1)


# create window and canvas to display our game of life in
top = tk.Tk()
canvas = tk.Canvas(top, bg='white', height=height, width=width)
canvas.pack()

while True:
    # delete all of the rectangles that have already been created so we can display the next iteration
    canvas.delete("all")
    # for every cell, see if it's supposed to be filled in (a 1) if it is, create a new rectangle using
    # square_size to determine placement on the canvas, by doing it this way, we can change the resolution just by
    # changing square size above
    for x in range(0, grid_size-1):
        for y in range(0, grid_size-1):
            if grid[x][y]:
                canvas.create_rectangle(x*square_size, y*square_size, x*square_size + square_size, y*square_size +
                                        square_size, fill="black")
    # get the next iteration of the game and save it to grid, then wait .1 seconds before updating the screen
    grid = iterate(grid)
    time.sleep(.1)
    top.update_idletasks()
    top.update()
