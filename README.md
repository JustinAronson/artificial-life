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
After a short wait, the simulation should appear in a separate window.

Simulation specific variables, such as the number of links in the snake, the range that the joints can move in, and the number of generations that evolve are determined in the file constants.py, located in the main folder. Feel free to change these.

# Brain and Body Generation
Links and neurons were generated according to the following diagram: [Assignment 7 Diagram.pdf](https://github.com/JustinAronson/artificial-life/files/10789815/Assignment.7.Diagram.pdf). 

At least one sensor neuron will be generated in every iteration of the simulation. If no links have been sensor neurons, the first time the generation algorithm reaches the maximum tree depth it will assign the link to be a sensor neuron. Motor neurons are generated for every joint in the robot, for a total of (number of links - 1) joints. The number of hidden neurons is specified in the constants.py file. Hidden neurons will always be generated in a single layer, receive input from all sensor neurons, and output to all motor neurons. As such, each sensor neuron will affect all motor neurons.

Links can be generated in any direction except for the negative z direction, and bodies are thus able to fill 3D space. Links do not intersect upon generation, although with joint motion they may intersect each other.

# Simulation Overview
The simulation submitted for Assignment 7 used the constants found in constants.py. The bodies were not evolved.

# Citations
Code for this reposity is based on the following:

[ludobots](https://www.reddit.com/r/ludobots/)

[pybullet](https://pybullet.org/wordpress/)

[pyrosim](https://github.com/ccappelle/pyrosim)
