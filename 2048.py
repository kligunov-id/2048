from tkinter import Tk, Button

from models import Cell, VisibleField, Direction

width = 1525
height = 860

def bind_keyboard(widget):
    activations = {
        "up": ("w", "Up"),
        "down": ("s", "Down"),
        "left": ("a", "Left"),
        "right": ("d", "Right"),
        "exit": ("e", "q", "Escape"),
        "restart": ("r", ),
    }
    actions = {
        "up": lambda: field.move(Direction.UP),
        "down": lambda: field.move(Direction.DOWN),
        "left": lambda: field.move(Direction.LEFT),
        "right": lambda: field.move(Direction.RIGHT),
        "exit": lambda: exit(0),
        "restart": lambda: field.reset(),  
    }
    def on_press(event):
        for alias, activators in activations.items():
            if event.keysym in activators:
                actions[alias]()
    widget.bind("<KeyPress>", on_press)


if __name__ == "__main__":

    root = Tk()
    root.attributes('-fullscreen', True)

    field = VisibleField(root)
    field.reset()
    
    start_button = Button(root, text="Restart", command=field.reset, width = 18, height=2, font=("Noto Sans Mono", 20))
    start_button.place(x=1200, y=60)

    save_button = Button(root, text="Save", command=field.save, width = 18, height=2, font=("Noto Sans Mono", 20))
    save_button.place(x=1200, y=150)

    load_button = Button(root, text="Load", command=field.load, width = 18, height=2, font=("Noto Sans Mono",  20))
    load_button.place(x=1200, y=240)
    
    bind_keyboard(root)

    root.mainloop()
