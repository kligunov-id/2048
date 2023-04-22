from random import choice
from tkinter import Canvas
from tkinter.font import Font
from math import log2
from matplotlib.cm import get_cmap
from matplotlib.colors import rgb2hex
from enum import Enum

class Direction(Enum):
    UNSET = "unset"
    LEFT = "left"
    UP = "up"
    RIGHT = "right"
    DOWN = "down"

class Cell:

    bgcolor = "#ccbacc"
    side = 200
    colormap = get_cmap("autumn", 10)

    @classmethod
    def color(cls, value):
        if value == 0:
            return cls.bgcolor
        i = int(log2(value)) % 10
        if i == 0:
            i = 10
        return rgb2hex(cls.colormap(10 - i))

    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.label = canvas.create_rectangle(x, y, x + self.side, y + self.side, fill=self.bgcolor, outline=self.bgcolor)
        self.value = 0
        self.font = Font(size=32, family="Noto Sans Mono")
        self.text = canvas.create_text(x + self.side//2, y + self.side//2, font=self.font)

    def update(self, value):
        self.value = value
        self.canvas.itemconfig(self.text, text=('' if value == 0 else str(value)))
        self.canvas.itemconfig(self.label, fill=self.color(value))

class Field:

    def __init__(self):
        self.grid = [[0 for j in range(4)] for i in range(4)]
        self.score = 0
        self.direction = Direction.UNSET
    
    def rotate_index(self, i, j):
        if self.direction == Direction.LEFT:
            return i, j
        elif self.direction == Direction.RIGHT:
            return i, 3 - j
        elif self.direction == Direction.UP:
            return j, i
        elif self.direction == Direction.DOWN:
            return 3 - j, i
    
    def get(self, i, j):
        i, j = self.rotate_index(i, j)
        return self.grid[i][j]

    def set(self, i, j, value):
       i, j = self.rotate_index(i, j)
       self.grid[i][j] = value

    def move_row(self, i):
        empty = 0
        for j in range(4):
            value = self.get(i, j)
            if value:
                self.set(i, empty, value)
                empty += 1
        for j in range(empty, 4):
            self.set(i, j, 0)

    def merge(self, i):
        for j in range(3):
            if self.get(i, j) == self.get(i, j + 1):
                self.set(i, j, 2 * self.get(i, j))
                self.set(i, j + 1, 0)

                self.score += self.get(i, j)

    def move(self, direction):
        old_grid = [grid_row.copy() for grid_row in self.grid]
        self.direction = direction
        for i in range(4):
            self.move_row(i)
            self.merge(i)
            self.move_row(i)
        self.direction = Direction.UNSET
        if old_grid != self.grid:
            self.spawn_new()

    def reset(self):
        self.grid = [[0 for j in range(4)] for i in range(4)]
        self.score = 0

        self.spawn_new()
        self.spawn_new()
    
    def get_empty(self):
        empty = []
        for i in range(4):
            for j in range(4):
                if not self.grid[i][j]:
                    empty.append((i, j))
        return empty

    def spawn_new(self, sample=[2] * 9 + [4]):
        empty = self.get_empty()
        if not empty:
            return
        i, j = choice(empty)
        self.grid[i][j] = choice(sample)
    
    def is_over(self):
        for i in range(4):
            for j in range(4):
                if not self.grid[i][j]:
                    return False
                if i < 3 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
                if j < 3 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
        return True

    def save(self, filename=".save"):
        with open(filename, "w") as save:
            save.write(str(self.score) + '\n')
            for grid_row in self.grid:
                save.write(' '.join([str(value) for value in grid_row]) + '\n')

    def load(self, filename=".save"):
        with open(filename, "r") as save:
            dump = save.readlines()
            self.score = int(dump[0])
            for i in range(4):
                self.grid[i] = [int(value) for value in dump[i + 1].split()]

class VisibleField(Field):
    
    margin = 15
    width = 1525
    height = 860

    def __init__(self, root):
        canvas = Canvas(root, width=self.width, height=self.height, bg='#ccaacc')
        canvas.pack()

        self.cells = [[Cell(canvas, *self.cell_position(i, j)) for j in range(4)] for i in range(4)]

        self.move = self.add_auto_update(self.move)
        self.spawn_new = self.add_auto_update(self.spawn_new)
        self.reset = self.add_auto_update(self.reset)
        self.load = self.add_auto_update(self.load)

    def cell_position(self, i , j):
        x = self.margin * (j + 1) + Cell.side * j
        y = self.margin * (i + 1) + Cell.side * i
        return x, y

    def update(self):
        for cell_row, grid_row in zip(self.cells, self.grid):
            for cell, value in zip(cell_row, grid_row):
                cell.update(value)

    def add_auto_update(self, function):
        def f_with_update(*args, **kwargs):
            function(*args, **kwargs)
            self.update()
        return f_with_update
