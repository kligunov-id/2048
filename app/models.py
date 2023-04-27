import random
import tkinter as tk
from tkinter.font import Font

from math import log2
from enum import Enum
from app.config import to_container

from matplotlib.cm import get_cmap
from matplotlib.colors import rgb2hex

class Action(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    RESET = "reset"
    SAVE = "save"
    LOAD = "load"
    START_AI = "start_ai"
    STOP_AI = "stop_ai"
    QUIT = "quit"

class Direction(Enum):
    UNSET = -1
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

class Cell:

    def color(self, value):
        if value == 0:
            return self.cell_config.background_color
        i = int(log2(value)) % self.cell_config.colormap.divisions
        if i == 0:
            i = self.cell_config.colormap.divisions
        return rgb2hex(self.colormap(self.cell_config.colormap.divisions - i))

    def __init__(self, canvas, cell_config, x, y):
        self.canvas = canvas
        self.cell_config = cell_config
        self.colormap = get_cmap(
            self.cell_config.colormap.name,
            self.cell_config.colormap.divisions)

        self.label = canvas.create_rectangle(
            x,
            y,
            x + self.cell_config.side_size,
            y + self.cell_config.side_size,
            fill=self.cell_config.background_color,
            outline=self.cell_config.background_color)
        self.font = Font(**to_container(self.cell_config.font))
        self.text = canvas.create_text(
            x + self.cell_config.side_size//2,
            y + self.cell_config.side_size//2,
            font=self.font)

    def update(self, value):
        self.canvas.itemconfig(self.text, text=('' if value == 0 else str(value)))
        self.canvas.itemconfig(self.label, fill=self.color(value))

class CorruptedSaveFileError(Exception):
    pass

class Field:

    def __init__(self, config):
        self.config = config
        self.n = config.field_size
        self.grid = [[0 for j in range(self.n)] for i in range(self.n)]
        self.score = 0
        self.direction = Direction.UNSET
        self.cell_changes_count = 0
    
    def rotate_index(self, i, j):
        if self.direction == Direction.LEFT or self.direction == Direction.UNSET:
            return i, j
        elif self.direction == Direction.RIGHT:
            return i, self.n - 1 - j
        elif self.direction == Direction.UP:
            return j, i
        elif self.direction == Direction.DOWN:
            return self.n - 1 - j, i
    
    def get(self, i, j):
        i, j = self.rotate_index(i, j)
        return self.grid[i][j]

    def set(self, i, j, value):
       i, j = self.rotate_index(i, j)
       if self.grid[i][j] != value:
           self.grid[i][j] = value
           self.cell_changes_count += 1

    def move_row(self, i):
        first_empty_j = 0
        for j in range(self.n):
            value = self.get(i, j)
            if value:
                self.set(i, first_empty_j, value)
                first_empty_j += 1
        for j in range(first_empty_j, self.n):
            self.set(i, j, 0)

    def merge(self, i):
        for j in range(self.n - 1):
            if self.get(i, j) == self.get(i, j + 1):
                self.set(i, j, 2 * self.get(i, j))
                self.set(i, j + 1, 0)
                self.score += self.get(i, j)

    def move(self, direction):
        self.cell_changes_count = 0
        self.direction = direction
        for i in range(self.n):
            self.move_row(i)
            self.merge(i)
            self.move_row(i)
        self.direction = Direction.UNSET
        if self.cell_changes_count:
            self.spawn_new()

    def reset(self):
        self.grid = [[0 for j in range(self.n)] for i in range(self.n)]
        self.score = 0

        self.spawn_new()
        self.spawn_new()
    
    def get_empty_cells(self):
        empty_cells = []
        for i in range(4):
            for j in range(4):
                if not self.get(i, j):
                    empty_cells.append((i, j))
        return empty_cells

    def spawn_new(self, sample=[2] * 9 + [4]):
        empty_cells = self.get_empty_cells()
        if not empty_cells:
            return
        i, j = random.choice(empty_cells)
        self.set(i, j, random.choice(sample))

    def is_over(self):
        for i in range(self.n):
            for j in range(self.n):
                if not self.grid[i][j]:
                    return False
                if i + 1 < self.n and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
                if j + 1 < self.n and self.grid[i][j] == self.get[i][j + 1]:
                    return False
        return True

    def save(self, filename=None):
        if filename is None:
            filename = self.config.save_path
        with open(filename, "w") as save:
            save.write(str(self.score) + '\n')
            for grid_row in self.grid:
                save.write(' '.join([str(value) for value in grid_row]) + '\n')

    def load(self, filename=None):
        if filename is None:
            filename = self.config.save_path
        dump = open(filename, "r").readlines()
        if len(dump) < self.n + 1:
            raise CorruptedSaveFileError(f"Save file too short, should have {self.n + 1} lines")
        try:
            self.score = int(dump[0])
            for i in range(self.n):
                if len(dump[i + 1].split()) == self.n:
                    self.grid[i] = [int(value) for value in dump[i + 1].split()]
                else:
                    raise CorruptedSaveFileError(f"Lines should contain exactly {self.n} integeres")
        except ValueError:
            raise CorruptedSaveFileError(f"Save file allows only integeres")

class VisibleField(Field):

    def __init__(self, root, config):
        super().__init__(config)
        self.layout_config = config.field_layout
        self.save_path = config.save_path

        canvas = tk.Canvas(root,
            width=self.layout_config.width,
            height=self.layout_config.height,
            bg=self.layout_config.background_color)
        canvas.pack()

        self.cells = [[Cell(canvas,
                            self.layout_config.cells,
                            *self.cell_position(i, j))
                        for j in range(self.n)] for i in range(self.n)]

    def cell_position(self, i , j):
        x = self.layout_config.cell_margin * (j + 1) + self.layout_config.cells.side_size * j
        y = self.layout_config.cell_margin * (i + 1) + self.layout_config.cells.side_size * i
        return x, y

    def set(self, i, j, value):
        i, j = self.rotate_index(i, j)
        if self.grid[i][j] != value:
            self.grid[i][j] = value
            self.cells[i][j].update(value)
            self.cell_changes_count += 1

    def update_cells(self):
        for i in range(self.n):
            for j in range(self.n):
                self.cells[i][j].update(self.grid[i][j])

    def reset(self):
        super().reset()
        self.update_cells()

    def load(self, filename=None):
        super().load(filename)
        self.update_cells()
