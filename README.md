# Description

This repository contains my submission for CS 396 Artificial Life. This repository is based on the [ludobots](https://www.reddit.com/r/ludobots/) course.

# System Dependencies
This repository is configured for a Mac machine running macOS. Machines running other operating systems will need to edit various os commands. Visit [ludobots](https://www.reddit.com/r/ludobots/) for machine specific instructions.

# Run and Installation Instructions
This repository requires [Python 3](https://www.python.org/downloads/). 

To run the simulation, first copy the entire repository from github. 

Navigate to the snakes branch, and run the command
```bash 
python3 search.py
```
After a short wait, the final evolved simulation should appear in a separate window.

Simulation specific variables, such as the number of links in the snake, the range that the joints can move in, and the number of generations that evolve are determined in the file constants.py, located in the main folder. Feel free to change these.

# Simulation Overview
The simulation submitted for Assignment 6 used the constants found in constants.py. A population size of 1 was simulated over 5 generations. Each snake had a motor joint range of 0.2. The snakes had a random number of sensor neurons, but a fixed number of hidden neurons, 4, that connected the sensors to the motors. Each link of the snake has a motor neuron. Links that function as sensor neurons are colored green, while links that are not sensors are colored blue.

The snakes were evolved with a fitness function that prioritized robots that minimized the euclidean distance between themselves and the point (-100, -100).

# Citations
Code for this reposity is based on the following:
[ludobots](https://www.reddit.com/r/ludobots/)
[pybullet](https://pybullet.org/wordpress/)
[pyrosim](https://github.com/ccappelle/pyrosim)
