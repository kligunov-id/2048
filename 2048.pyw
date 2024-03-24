from app.app import App
from app.config import Config

def main():
    with Config() as config:
        app = App(config)
        app.mainloop()

if __name__ == "__main__":
    main()
