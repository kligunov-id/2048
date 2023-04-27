2048
------------

This is a simple Python Tkinter implementation of the famous game.


### To run

Simply execute `python 2048.py`.


### Controls

Both `WASD` and arrow keys supported. `Esc`,  `E` or `Q` to exit, `R` to restart.
In case other bindings (even for other actions) are desired, edit them under `conf/config.yaml`. List of all available actions and their aliases is defined by the `Actions` enum of `app/models.py` module.

Multi-key bindings are not implemented (not even Ctrl + Key combinations, although Ctrl by itsef is a valid option).

### Save option

Saves are stored in a ```.save``` text file which can be manually altered (so you can cheat in anything, even odd values).

In case it somehow gets corrupted you can simply delete it.

### Config files

All of the setting and constants the programm uses are stored under `conf/` folder. Feel free to change any of those options. But note however, that after fetching updates from the repo any changes will be likely erased by them, so you might prefer a manual merge.

Also layout and appearence definitions (e.g colors and fonts) can be found in theese files, so if you can make app look less depressing you should probably do so.

### User-programmed bots

If you wish to try out your bot in this environment, replace the content of `app/bot.py` file with your own. The protocol is simple: your module should define an ___object___ named `model` which should have an implementation of the `model.act(grid)` function. This function should accept a two-dimensional Python list of values for each cell in the grid and return a number between 1 and 4 which corresponds to the move your bot is willing to make. The mapping of numbers to directions is done via the `Direction` enum defined in `app/models.py`.

### Future plans

- separate API for bot training
- smooth animations & redesign, scoring
- new and exotic game modes
- RL neural network bot instead of randomizer dummy
