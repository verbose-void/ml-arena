# ML_Arena
A fully custom simulation environment that interchangeably compares reinforcement learning models. Has a full blown API for modularity of algorithms, built in general genetic neural network library, and other utilities for training and testing.

# Training Process:

### Fitness Evaluation:
> After experimenting with Fixed-Topology Neuro-Evolution within this environment, I've found that neglecting to discount detrimental fitness factors, it will fail to develop any sort of effective policy. After hours of trial and error, passing detriment values under a logarithm seems to suffice as it asserts that the detriments don't have such a serious impact on it's overall score, but rather it heavyily rewards minimizing it. You can view the actual method inside [Fitness Pawn](https://github.com/McCrearyD/ML_Arena/blob/master/actors/pawns/fitness_pawn.py) class under "calculate_fitness".

# General Info

### Versions:
- Built in [python3](https://www.python.org/downloads/).

### Libraries Required:
- [Arcade](http://arcade.academy/)
- [Numpy](http://www.numpy.org/)

### Usage:
- Clone this repository. `git clone https://github.com/McCrearyD/ML_Arena.git`
- To run any simulation, run `python3 -u main.py` inside the main directory.
- Follow the terminal instructions to run any type of simulation.
- To run all test assertions & test environment, run `python3 -u test.py` inside the main directory.
- To view a graph for any saved population, run `python3 -u visualize.py` inside the main directory.

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

# Main Simulation Keys
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
|N|(Toggle) Visually display the currently focused creature(s) Neural Networks|Evolution|
|P|(Toggle) Speed up all gameplay. Updates per frame can be changed in `environment.py > class Environment > var('speed_up_cycles')`|Global|

<br>

# Test Environment Keys
|Key(s)|Description|
|---|---|
|BACKSPACE|Next generation|
|ESCAPE|Randomize goal location|

<br>

## Showcase:

|||
|:-------------------------:|:-------------------------:|
|**Custom Network Visualization**|**Freeplay**|
|<img alt="1" src="https://i.gyazo.com/17d1f8366c614b86c0c5fce5269027b7.png">|<img alt="1" src="https://i.gyazo.com/0baf14ecd33ec3a7668972bf08dd7f24.gif">|
|**Evolutionary Training**|**Statistical Bias Balancing**|
|<img alt="1" src="https://i.gyazo.com/7948da19c26cd46e7455a111098f4259.gif">|<img alt="1" src="https://i.gyazo.com/c40352df2597a940ba28a381384ed303.gif">|
|**Test Environment**|**Non-Graphical Simulation w/ Generational Reports**|
|<img alt="1" src="https://i.gyazo.com/21c3eb000d70a10994b19016745e5595.gif">|<img alt="1" src="https://i.gyazo.com/c4e94273f0df16d01337c6bbabe590d6.gif">
|**Saved Population Visualization**||
|<img alt="1" src="https://i.gyazo.com/dbca70f374a4d88d5a80f88e6c93c78b.gif">||
