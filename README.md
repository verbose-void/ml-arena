# ML_Arena
Compare predictive modes &amp; predispositions to sway learning / evolutionary traits in an asteroids-like arena.

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
|OPEN-BRACKET|Show all pawns in the population|Evolutionary Training|
|ESCAPE|End training session and prompt to save progress|Evolutionary Training|
