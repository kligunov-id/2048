from tkinter import Tk, Button
from keyboard import listener

from models import Cell, VisibleField, LEFT, RIGHT, UP, DOWN

width = 1525
height = 860

def gameloop(field):
    listener.unlock()
    field.reset()
    while True:
        root.update()
        if listener.is_active("exit"):
            exit(0)
        elif listener.is_active("left"):
            listener.lock()
            field.move(LEFT)
        elif listener.is_active("up"):
            listener.lock()
            field.move(UP)
        elif listener.is_active("right"):
            listener.lock()
            field.move(RIGHT)
        elif listener.is_active("down"):
            listener.lock()
            field.move(DOWN)
        elif listener.is_active("restart"):
            listener.lock()
            field.reset()
        elif not listener.is_any_active(ignore_lock=True):
            listener.unlock()

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
