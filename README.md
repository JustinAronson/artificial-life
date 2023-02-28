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

# Evolution
After each generation was simulated, either the brain or body of the robot was mutated. One of the two was mutated at each generation, and both were never mutated in the same generation.

# Brain Evolution
When the brain mutated, the weight of one of the synapses sending information from a sensor neuron to a hidden neuron was randomized, as well as the weight of one of the synapses sending information from a hidden neuron to a motor neuron. Additionally, there was a 10% chance that a hidden neuron would be either deleted or gained each time the brain mutated. This hidden neuron would be connected to all sensor neurons and motor neurons. The following diagram demonstrates the connections lost from gaining or losing a hidden neuron: 

<img src="https://github.com/JustinAronson/artificial-life/blob/3d-creatures/Changing%20Hidden%20Neurons.jpg" width = 300 height = whatever>

Hidden neurons are mutated such that there is always one hidden neuron in the brain.

# Body Evolution
When the body mutated, one of the following could happen with related weights:

Chance (Percent)  | Effect
------------- | -------------
10  | Add links
10  | Remove link
20  | Change non-sensing link to sensing link
20  | Change sensing link to non-sensing link
40  | Change link size

These are all mutually exclusive events (one generation of robots cannot have both an add link and remove link mutation).
### Add links

This mutation has a 60% chance to add a single link, a 30% chance to add two links, and a 10% chance to add three links to the creature. It adds links to any open face of the creature. The open face does not need to be at the end of a branch. All added links follow the rules of body generation, with the exception of the following rule: Links are not added past the max depth of the robot. Mutated links are able to be added beyond the depth specified in constants.py. Diagram depicting this addition:

<img src="https://github.com/JustinAronson/artificial-life/blob/3d-creatures/Adding%20link.jpg" width = 300 height = whatever>

### Remove link
          
This mutation removes a single random link from the creature. Removed links are always at the end of a branch.
### Change non-sensing link to sensing link
          
This mutation changes a single random non-sensing link into a sensing link. Synaptic weights are randomized.
### Change sensing link to non-sensing link
          
This mutation changes a single random sensing link into a non-sensing link. The sensor neuron associated with the link is deleted.
### Change link size
          
This mutation changes a random link's size in the creature. The relative positions of the links upstream to it in the creature remain the same. When updating the link's size causes an intersection between any two links in the creature, the mutation is aborted and the link remains at its current size. Diagram depicting this check:

<img src="https://github.com/JustinAronson/artificial-life/blob/3d-creatures/Changing%20link%20size.jpg" width = 300 height = whatever>

# Simulation Overview
The simulation submitted for Assignment 7 used the constants found in constants.py. The bodies were evolved by mutating a parent generation, and picking the robots with the best fitness from each family. Fitness was determined by the robot's Euclidean distance to the point -100, -100. A smaller distance was prefered.

## Fitness Values at each Generation
The following graph contains the best fitness value at each generation for 5 robots over 50 generations, with a population size of 50. A smaller fitness value was preferred. ![Graph](https://github.com/JustinAronson/artificial-life/blob/3d-creatures/Screen%20Shot%202023-02-28%20at%2012.11.16%20AM.png)

A popular strategy used by robots in this simulation was building tall robots which fell over in the (-x, -y) direction. Future fitness functions will test for robot movement after a certain time step to make this strategy more difficult.

# Citations
Code for this reposity is based on the following:

[ludobots](https://www.reddit.com/r/ludobots/)

[pybullet](https://pybullet.org/wordpress/)

[pyrosim](https://github.com/ccappelle/pyrosim)
