# pyWordle

pyWordle is a Wordle clone that can be played via the command line.

It has 2 game rendering modes, ASCII text and emojis.

## Requirements

pyWordle is tested with:

- Python 3.10

It is recommended to use a python version manager like pyenv to manage your python installs:

```shell
pyenv install 3.10.0
pyenv local 3.10.0
```

## Getting Started

### Installing dependencies

```shell
pip install poetry
poetry install
```

### Running the default game

```shell
poetry run python app.py
```

### Tweaking game parameters

```python
from pywordle import PyWordle, AsciiRenderer, EmojiRenderer
board = PyWordle(length=5, attempts=6, renderer=AsciiRenderer)
board.start_game()
```

# Implementation Details

## Word list

The word list is the CSW15 word list. On initial run, PyWordle attempst to fetch this file and saves it locally. Each PyWordle instance will filter though this text file to generate a list of valid words. Do note that there is no preference to "regular" words, any valid word can be chosen as the secret answer.

## Renderers

There are 2 `Renderer` subclasses provided with PyWordle, `AsciiRenderer` and `EmojiRenderer`. The base logic is defined in `Renderer`, and you should subclass it to customise it to your preferences. Rendering logic is seperate from the board state, and it should be possible to implement a GUI Renderer using PyGame or similar libraries (Todo) that hooks into the default `PyWordle` instance.

