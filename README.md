# ML_Arena
Compare predictive modes &amp; predispositions to sway learning / evolutionary traits in an asteroids-like arena.

## CURRENTLY UNDER REFACTORY, THIS DOCUMENTATION WILL CHANGE SOON.

### Versions:
- Built in [python3](https://www.python.org/downloads/).

### Libraries Required:
- [Arcade](http://arcade.academy/)
- [Numpy](http://www.numpy.org/)

### Usage:
- Clone this repository. `git clone https://github.com/McCrearyD/ML_Arena.git`
- To test functionality of the **dynamically scripted pawn** or **player controlled pawn**, run the "environment.py" file with python. `python3 -u environment.py`.
- To create, load, and train **evolutionary neural network** populations, run the "evolve.py" file with python. `python3 -u evolve.py`.

#### *Note: When you run these files, the console will prompt you with directions for creating, loading, & saving populations.*

<br>
<br>

|Key(s)|Description|Context|
|---|---|---|
|W, A, S, D|Movement|Player Controlled Pawn|
|LEFT, UP, RIGHT, DOWN|Directional movement|Player Controlled Pawn|
|Q|Shield|Player Controlled Pawn|
|SHIFT|Long-range laser|Player Controlled Pawn|
|SPACE|Short-range laser|Player Controlled Pawn|
|OPEN-BRACKET|Draw all pawns in every match|All Types|
|CLOSE-BRACKET|Show connections between all on-screen pawns|All Types|
|ESCAPE|End training session and prompt to save progress|Evolutionary Training|
|BACKSPACE|Force end the current generation|Evolutionary Training|


## Showcase:
#### Base Gameplay:
![https://i.gyazo.com/b2fd1b4b7dbb1044a2218b12d565b063.gif](https://i.gyazo.com/b2fd1b4b7dbb1044a2218b12d565b063.gif)

#### Evolutionary Training:
![https://i.gyazo.com/c8d974d828994b937921119e4ebde1ed.gif](https://i.gyazo.com/c8d974d828994b937921119e4ebde1ed.gif)
