from pynput import keyboard
from pynput.keyboard import Key

class Listener:
    activations = {
        "up": ("w", Key.up),
        "down": ("s", Key.down),
        "left": ("a", Key.left),
        "right": ("d", Key.right),
        "exit": ("e", Key.esc),
        "restart": ("r", ),  
    }

    def __init__(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        self.locked = False

        self.activated = {}
        for key in self.activations:
            self.activated[key] = False

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def is_active(self, name: str, ignore_lock=False) -> bool:
        if not ignore_lock and self.locked:
            return False
        return self.activated[name]

    def is_any_active(self, ignore_lock=False) -> bool:
        if not ignore_lock and self.locked:
            return False
        for name in self.activated:
            if self.activated[name]:
                return True
        return False

    def set_key(self, key, value: bool):
        for name in self.activations:
            if key in self.activations[name]:
                self.activated[name] = value

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
