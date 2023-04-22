from tkinter import Tk, Button
from models import VisibleField, Direction, Action
from bot import model

class App:
    width = 1525
    height = 860

    activations = {
        "up": ("w", "Up"),
        "down": ("s", "Down"),
        "left": ("a", "Left"),
        "right": ("d", "Right"),
        "quit": ("e", "q", "Escape"),
        "reset": ("r", ),
    }

    def __init__(self):
        self.root = Tk()
        self.root.attributes('-fullscreen', True)

        self.field = VisibleField(self.root)
        self.field.reset()
        
        self.actions = {
            Action.UP: lambda: self.field.move(Direction.UP),
            Action.DOWN: lambda: self.field.move(Direction.DOWN),
            Action.LEFT: lambda: self.field.move(Direction.LEFT),
            Action.RIGHT: lambda: self.field.move(Direction.RIGHT),
            Action.RESET: lambda: self.field.reset(),
            Action.SAVE: lambda: self.field.save(), 
            Action.LOAD: lambda: self.field.load(),
            Action.START_AI: lambda: self.start_bot(), 
            Action.STOP_AI: lambda: self.stop_bot(),   
            Action.QUIT: lambda: exit(0),
        }
        self.bind_keyboard()

        self.buttons = {}
        self.init_buttons()

        self.bot_running = False

    def init_buttons(self):
        style = dict(width=18, height=2, font=("Noto Sans Mono", 20))
        self.buttons["reset"] = Button(self.root, text="Restart", command=self.actions[Action.RESET], **style)
        self.buttons["reset"].place(x=1200, y=60)
        self.buttons["save"] = Button(self.root, text="Save", command=self.actions[Action.SAVE], **style)
        self.buttons["save"].place(x=1200, y=150)
        self.buttons["load"] = Button(self.root, text="Load", command=self.actions[Action.LOAD], **style)
        self.buttons["load"].place(x=1200, y=240)
        self.buttons["start_ai"] = Button(self.root, text="Start AI", command=self.actions[Action.START_AI], **style)
        self.buttons["start_ai"].place(x=1200, y=350)
        self.buttons["stop_bot"] = Button(self.root, text="Stop AI", command=self.actions[Action.STOP_AI], **style)
        self.buttons["stop_bot"].place(x=1200, y=440)
        self.buttons["quit"] = Button(self.root, text="Quit", command=self.actions[Action.QUIT], **style)
        self.buttons["quit"].place(x=1200, y=550)

    def bind_keyboard(self):
        def on_press(event):
            for alias, activators in self.activations.items():
                if event.keysym in activators:
                    self.actions[Action(alias)]()
        self.root.bind("<KeyPress>", on_press)
    
    def start_bot(self):
        if self.bot_running:
             return
        self.bot_running = True
        self.step_bot()

    def stop_bot(self):
        self.bot_running = False

    def step_bot(self):
        if not self.bot_running:
            return
        move = Direction(model.act(self.field.grid))
        self.field.move(move)
        self.root.after(200, self.step_bot)

    def mainloop(self):
        self.root.mainloop()

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
