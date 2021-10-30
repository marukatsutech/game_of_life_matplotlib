# Conway's Game of Life (matplotlib) (without clear ax)
import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


def boundary_row(n):    # Boundary condition
    if n >= row:
        return 0
    elif n < 0:
        return row - 1
    else:
        return n


def boundary_col(n):    # Boundary condition
    if n >= col:
        return 0
    elif n < 0:
        return col - 1
    else:
        return n


def eval_neighbours(rw, cl):
    global cells0
    result = 0
    for k in range(8):
        result = result + cells0[boundary_row(rw + neighbours[k][0]), boundary_col(cl + neighbours[k][1])]
    return int(result)


def next_generation():
    global cells0, cells1
    for i in range(row):
        for j in range(col):
            cell = cells0[i][j]
            result = eval_neighbours(i, j)
            if cell == 1:
                if result < 2:
                    cells1[i][j] = 0
                elif result == 2 or result == 3:
                    cells1[i][j] = 1
                else:
                    cells1[i][j] = 0
            else:
                if result == 3:
                    cells1[i][j] = 1
    # Reflect to cells0
    cells0 = copy.deepcopy(cells1)


def initialize_cells0():
    global cells0
    for i in range(row):
        for j in range(col):
            cells0[i][j] = random.randint(0, 1)


def update(f):
    global cells0, cells1, x, y, scat, tx_step
    tx_step.set_text("Step=" + str(f))
    # evaluate cells
    next_generation()
    # Draw cells
    x.clear()
    y.clear()
    for i in range(row):
        for j in range(col):
            if cells0[i][j] == 1:
                y.append(i + cells_offset)
                x.append(j + cells_offset)
    scat.set_offsets(np.column_stack([x, y]))


# Global variables
x_min = 0.
x_max = 50.
y_min = 0
y_max = 50

row = 50
col = 50
cells0 = np.zeros((row, col))   # Cells plane
cells1 = np.zeros((row, col))   # Cells plane buffer
# Relative row and column of neighbours
neighbours = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

cells_offset = 0.5   # Offset in plt.scatter

# Set initial live cells
initialize_cells0()

# Generate figure and axes
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title("Conway's Game of Life")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_aspect("equal")
ax.grid()

# Generate items
x = []
y = []
scat = plt.scatter(x, y, marker='s', s=6)
tx_step = ax.text(x_min, y_max * 0.95, "Step=" + str(0))

# Draw animation
anim = animation.FuncAnimation(fig, update, interval=100)
plt.show()
