from pynput import keyboard
from pynput.keyboard import Key

class Listener:
    activations = {
        "up": ("w", Key.up),
        "down": ("s", Key.down),
        "left": ("a", Key.left),
        "right": ("d", Key.right),
        "exit": ("e", "q", Key.esc),
        "restart": ("r", ),  
    }

    def __init__(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

        self.pressed = {}
        self.locked = {}
        for name in self.activations:
            for key in self.activations[name]:
                self.pressed[key] = False
                self.locked[key] = False

    def lock(self, key):
        self.locked[key] = True

    def unlock(self, key):
        self.locked[key] = False

    def set_key(self, key, value: bool):
        self.pressed[key] = value
        if not value:
            self.unlock(key)
    
    def locking_check(self, name: str):
        for key in self.activations[name]:
            if self.pressed[key] and not self.locked[key]:
                self.lock(key)
                return True
        return False

    def on_press(self, key):
        if key is None:
           return
        try:
            self.set_key(key.char, True)
        except AttributeError:
            self.set_key(key, True)

    def on_release(self, key):
        if key is None:
           return
        try:
            self.set_key(key.char, False)
        except AttributeError:
            self.set_key(key, False)

listener = Listener()
