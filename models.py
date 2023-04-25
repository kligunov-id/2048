from random import choice
from tkinter import Canvas
from tkinter.font import Font
from math import log2
from matplotlib.cm import get_cmap
from matplotlib.colors import rgb2hex
from enum import Enum

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
        self.font = Font(size=32, family="Noto Sans Mono")
        self.text = canvas.create_text(x + self.side//2, y + self.side//2, font=self.font)

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
        i, j = choice(empty_cells)
        self.set(i, j, choice(sample))

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

    def save(self, filename=".save"):
        with open(filename, "w") as save:
            save.write(str(self.score) + '\n')
            for grid_row in self.grid:
                save.write(' '.join([str(value) for value in grid_row]) + '\n')

    def load(self, filename=".save"):
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

    margin = 15
    width = 1525
    height = 860

    def __init__(self, root, config):
        super().__init__(config)

        canvas = Canvas(root, width=self.width, height=self.height, bg='#ccaacc')
        canvas.pack()

        self.cells = [[Cell(canvas, *self.cell_position(i, j)) for j in range(4)] for i in range(4)]

    def cell_position(self, i , j):
        x = self.margin * (j + 1) + Cell.side * j
        y = self.margin * (i + 1) + Cell.side * i
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

    def load(self, filename=".save"):
        super().load(filename)
        self.update_cells()
