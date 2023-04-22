from tkinter import Tk, Button
from keyboard import listener

from models import Cell, VisibleField, LEFT, RIGHT, UP, DOWN

width = 1525
height = 860

def gameloop(field):
    field.reset()
    while True:
        root.update()
        if listener.locking_check("exit"):
            exit(0)
        elif listener.locking_check("left"):
            field.move(LEFT)
        elif listener.locking_check("up"):
            field.move(UP)
        elif listener.locking_check("right"):
            field.move(RIGHT)
        elif listener.locking_check("down"):
            field.move(DOWN)
        elif listener.locking_check("restart"):
            field.reset()

if __name__ == "__main__":

    root = Tk()
    root.attributes('-fullscreen', True)

    field = VisibleField(root)
    
    start_button = Button(root, text="Restart", command=field.reset, width = 18, height=2, font=("Noto Sans Mono", 20))
    start_button.place(x=1200, y=60)

    save_button = Button(root, text="Save", command=field.save, width = 18, height=2, font=("Noto Sans Mono", 20))
    save_button.place(x=1200, y=150)

    load_button = Button(root, text="Load", command=field.load, width = 18, height=2, font=("Noto Sans Mono",  20))
    load_button.place(x=1200, y=240)

    gameloop(field)
