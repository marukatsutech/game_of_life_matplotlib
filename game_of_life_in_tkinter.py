# Conway's Game of Life (matplotlib) (without clear ax)(embedded in tkinter)
import copy
import numpy as np
import random
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk


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


def clear_cells():
    global cells0, cells1, cnt
    for i in range(row):
        for j in range(col):
            cells0[i][j] = 0
            cells1[i][j] = 0
    cnt = 0
    tx_step.set_text("Step=" + str(cnt))
    draw_cell()


def randomize_cells0():
    global cells0
    for i in range(row):
        for j in range(col):
            cells0[i][j] = random.randint(0, 1)
    draw_cell()


def initialize_cells0():
    global cells0
    for i in range(row):
        for j in range(col):
            cells0[i][j] = random.randint(0, 1)


def draw_cell():
    global cells0, x, y, scat, s
    # For adjustment maker size
    bbox = fig.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width = bbox.width * fig.dpi
    height = bbox.height * fig.dpi
    print((width, height))
    x_size = width / (x_max - x_min)
    print(x_size)
    # draw cells
    x.clear()
    y.clear()
    s.clear()
    for i in range(row):
        for j in range(col):
            if cells0[i][j] == 1:
                y.append(i + cells_offset)
                x.append(j + cells_offset)
                s.append(x_size ** 2 * 0.08)
    scat.set_offsets(np.column_stack([x, y]))
    scat.set_sizes(s)


def on_change_window(e):
    if not on_play:
        draw_cell()


def switch():
    global on_play
    if on_play:
        on_play = False
    else:
        on_play = True


def update(f):
    global cells0, cells1, x, y, scat, tx_step, cnt
    if on_play:
        tx_step.set_text("Step=" + str(cnt))
        cnt += 1
        # evaluate cells
        next_generation()
        # Draw cells
        draw_cell()


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

on_play = False
cnt = 0

# Set initial live cells
initialize_cells0()

# Generate figure and axes
fig = Figure()
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
s = []  # maker size
scat = ax.scatter(x, y, marker='s', s=6)
tx_step = ax.text(x_min, y_max * 0.95, "Step=" + str(0))
draw_cell()

# Tkinter
root = tk.Tk()
root.title("Sample3")
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(expand=True, fill='both')

toolbar = NavigationToolbar2Tk(canvas, root)
canvas.get_tk_widget().pack()

# Play and pause button
btn_pp = tk.Button(root, text="Play/Pause", command=switch)
btn_pp.pack(side='left')

# Random button
btn_clr = tk.Button(root, text="Random", command=randomize_cells0)
btn_clr.pack(side='left')

# Clear button
btn_clr = tk.Button(root, text="Clear", command=clear_cells)
btn_clr.pack(side='left')

# Draw animation
anim = animation.FuncAnimation(fig, update, interval=100)
root.bind('<Configure>', on_change_window)
root.mainloop()
