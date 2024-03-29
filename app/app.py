import tkinter as tk
import app.models as models

from app.models import Direction, Action
from app.config import to_container
from app.bot import model

class App:

    def __init__(self, config):
        self.config = config

        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)

        self.field = models.VisibleField(self.root, self.config)
        self.field.reset()
        
        self.keyboard_controls = self.config.controls
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
            Action.QUIT: self.root.destroy,
        }
        self.bind_keyboard()

        self.buttons = {}
        self.init_buttons()

        self.bot_running = False

    def init_buttons(self):
        for button in self.config.buttons:
            self.buttons[button.name] = tk.Button(
                self.root,
                text=button.name,
                command=self.actions[Action(button.action)],
                **to_container(button.style))
            self.buttons[button.name].place(x=button.x, y=button.y)

    def bind_keyboard(self):
        def on_press(event):
            for action_alias, keysyms in self.keyboard_controls.items():
                if event.keysym in keysyms:
                    self.actions[Action(action_alias)]()
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
        self.root.after(self.config.bot_timeout_ms, self.step_bot)

    def mainloop(self):
        self.root.mainloop()
