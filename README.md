# ML_Arena
Compare predictive modes &amp; predispositions to sway learning / evolutionary traits in an asteroids-like arena.

### Versions:
- Built in [python3](https://www.python.org/downloads/).

### Libraries Required:
- [Arcade](http://arcade.academy/)
- [Numpy](http://www.numpy.org/)

### Usage:
- Clone this repository. `git clone https://github.com/McCrearyD/ML_Arena.git`
- To run any simulation, run `python3 -u main.py` inside the main directory.
- Follow the terminal instructions to run any type of simulation.

### Simulation Types:
- **Freeplay**: Freeplay allows you to create a single matchup using any type of pawn controller you'd like.
- **Evolution**: 
    - ***Adversarial***: Train a random (or load previous) population against another.
    - ***Other***: Train a random (or load previous) population against another pawn type (ie. dynamic or brainless).
- **Balance**: Run a balancing simulation for pawn statistical biases. Runs `x` match iterations concurrently and reports win/loss results for each bias.

### Indicators:
- Blue Pawn: If a pawn's color is blue, this means they have enabled their shield.
- Red Pawn: If they are red, this means their health is 0.
- Number Below Pawn: If a pawn has a number, this means they are a FitnessPawn. A fitness pawn is typically assigned to a neural network in order to judge how good they are. The higher = the better.
- Bar Above Pawn: Every pawn has a bar above their head that displays their health percentage. 
    - Green = +75%
    - Yellow = +50%
    - Red = -50%
- Red Laser: Long distance laser.
  - Lighter Red: Hasn't reached the minimum distance yet, if it collides with an enemy, they won't be damaged.
  - Darker Red: Fully charged laser, upon impact it will deal damage.
- Blue Laser: Short distance laser.
- Green Laser (Debug): A laser is highlighted green if it is the 'imminent laser' of the current player pawn.

<br>

|Key(s)|Description|Context|
|---|---|---|
|W, A, S, D|Movement|Player|
|LEFT, UP, RIGHT, DOWN|Directional movement|Player|
|Q|Shield|Player|
|SHIFT|Long-range laser|Player|
|SPACE|Short-range laser|Player|
|OPEN-BRACKET|Draw all pawns in every match|Global|
|CLOSE-BRACKET|Show connections between all on-screen pawns|Global|
|BACK-SLASH|Show pawn directional tracers|Global|
|ESCAPE|End simulation, if Evolutionary: Save populations under their names|Global|
|BACKSPACE|Force reset the environment. If Evolutionary: End the current generation|Global|

## Showcase:

|||
|:-------------------------:|:-------------------------:|
|**Custom Network Visualization**|**Freeplay**|
|<img width="1604" alt="1" src="https://i.gyazo.com/17d1f8366c614b86c0c5fce5269027b7.png">|<img width="1604" alt="1" src="https://i.gyazo.com/0baf14ecd33ec3a7668972bf08dd7f24.gif">|
|**Evolutionary Training**|**Statistical Bias Balancing**|
|<img width="1604" alt="1" src="https://i.gyazo.com/7948da19c26cd46e7455a111098f4259.gif">|<img width="1604" alt="1" src="https://i.gyazo.com/c40352df2597a940ba28a381384ed303.gif">|
