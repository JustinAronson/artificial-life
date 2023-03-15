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
Links are generated in a tree format. Links are placed on open faces of links: ![Links on open faces](https://user-images.githubusercontent.com/11809261/225104341-504f90e6-11d8-4be0-a486-9194c57af45b.PNG)

Links are placed until they reach a certain depth, specified in constants.py, from the root node. In this example, depth is 3. Links can be added to links with depth 0, 1, and 2, but no links can be added to a face of a link with depth 3. ![Depth](https://user-images.githubusercontent.com/11809261/225104761-98a6083d-a4dd-46f7-b9e1-86f491608ff2.PNG)
Note: the links in this diagram are named with their depth. Links in all future diagrams will be named with the link name used for pyrosim.

Links cannot be placed in the opposite direction that the tree branch they belong to has grown. In the following example, the link cannot be placed in the south direction because its branch (consisting of links 1, 2, and 4) has grown in the north direction. ![Direction](https://user-images.githubusercontent.com/11809261/225105252-12e2c933-afe5-4256-8cba-1e11e14524a4.PNG)

Links can function as sensors. Links with sensors are colored green, while links without are colored blue. At least one sensor neuron will be generated in every iteration of the simulation. If no links have been sensor neurons, the first time the generation algorithm reaches the maximum tree depth it will assign the link to be a sensor neuron. Motor neurons are generated for every joint in the robot, for a total of (number of links - 1) joints. The number of hidden neurons is specified in the constants.py file. Hidden neurons will always be generated in a single layer, receive input from all sensor neurons, and output to all motor neurons. As such, each sensor neuron will affect all motor neurons. Below is an example of how a body's sensors and neurons interact: ![Gen1](https://user-images.githubusercontent.com/11809261/225106066-65a5fd0c-5d70-4797-9e34-3c04996ad6ec.PNG)
We will be refering to this robot in the future. Let's call it Bob.


Links can be generated in any direction except for the negative z direction, and bodies are thus able to fill 3D space. Links do not intersect upon generation, although with joint motion they may intersect each other.

# Evolution
After each generation was simulated, either the brain or body of the robot was mutated. One of the two was mutated at each generation, and both were never mutated in the same generation. The body was mutated with the following probability, based on generation.

<img width="753" alt="Screen Shot 2023-03-14 at 10 07 18 PM" src="https://user-images.githubusercontent.com/11809261/225195155-a2a1ad22-77db-4a59-a382-7bf86e5cb57e.png">

As you can see, the bodies were mutated with about a 60% chance until the 200th generation. The chance that the body mutates falls until generation 400, where the body can no longer mutate. The brain mutates with probability (1-body mutation probability).

# Brain Evolution
When the brain mutated, the weight of one of the synapses sending information from a sensor neuron to a hidden neuron was randomized, as well as the weight of one of the synapses sending information from a hidden neuron to a motor neuron. Additionally, there was a 10% chance that a hidden neuron would be either deleted or gained each time the brain mutated. This hidden neuron would be connected to all sensor neurons and motor neurons. The following diagram demonstrates the connections lost when Bob loses a hidden neuron: 
![Gen2](https://user-images.githubusercontent.com/11809261/225107365-f1eb71e1-5c2e-48d1-9edb-cbf6e4467a54.PNG)
If Bob now gains a hidden neuron, he would simply return to his previous brain structure.

Hidden neurons are mutated such that there is always one hidden neuron in the brain.

# Body Evolution
When the body mutated, one of the following could happen with related weights:

Chance (Percent)  | Effect
------------- | -------------
20  | Change sensing link to non-sensing link
20  | Change non-sensing link to sensing link
10  | Add links
10  | Remove link
40  | Change link size

These are all mutually exclusive events (one generation of robots cannot have both an add link and remove link mutation).
### Change sensing link to non-sensing link
          
This mutation changes a single random sensing link into a non-sensing link. The sensor neuron associated with the link is deleted.

To visualize this change, let's say Bob underwent this mutation. His link 1 changes from a sensing link to a non-sensing link. His new body plan becomes:
![IMG_0903](https://user-images.githubusercontent.com/11809261/225108142-0dcac387-7777-4add-a04c-287353716900.PNG)
### Change non-sensing link to sensing link
          
This mutation changes a single random non-sensing link into a sensing link. Synaptic weights are randomized.

If Bob mutated his link 1 to again become a sensing link, his body plan would return to:
![Gen2](https://user-images.githubusercontent.com/11809261/225107365-f1eb71e1-5c2e-48d1-9edb-cbf6e4467a54.PNG)
### Add links

This mutation has a 60% chance to add a single link, a 30% chance to add two links, and a 10% chance to add three links to the creature. It adds links to any open face of the creature. The open face does not need to be at the end of a branch. All added links follow the rules of body generation, with the exception of the following rule: Links are not added past the max depth of the robot. Mutated links are able to be added beyond the depth specified in constants.py.

Here is Bob after undergoing an add links mutation:![IMG_0904](https://user-images.githubusercontent.com/11809261/225110367-9e0fbd73-9d86-4cc7-b021-c835a5b5e72b.PNG)
### Remove link
          
This mutation removes a single random link from the creature. Removed links are always at the end of a branch.

### Change link size
          
This mutation changes a random link's size in the creature. The relative positions of the links upstream to it in the creature remain the same. When updating the link's size causes an intersection between any two links in the creature, the mutation is aborted and the link remains at its current size.

If Bob were to undergo a change link size mutation: ![IMG_0905](https://user-images.githubusercontent.com/11809261/225108964-9aae1c0f-4b4f-450d-b74d-018816b387a1.PNG)

# Simulation Overview
The simulation submitted for the Final Project used the constants found in constants.py. The runs for seeds (20, 21, ... 28, 29) in the graph below can be repeated by running search.py. Other runs can be tested by changing the value used by ``` random.seed() ``` in search.py. 

The fitness of a robot was determined by the robot's Euclidean distance to the point -100, -100. A smaller distance was prefered. If the blue cube is a robot, its goal is to approach the yellow square:
![IMG_0909](https://user-images.githubusercontent.com/11809261/225109812-2ff7d8dd-73ff-4c8c-9481-416c424e44f9.PNG)

The bodies were evolved by mutating a parent generation to produce a child generation. Each child would have one mutation listed above that makes them differ from their parent. Each child would then be placed into the simulation. If it scored a smaller fitness than its parent, it would become the next parent for the next generation of robots. Otherwise, the parent would remain as the parent for the next generation.
For example, in this diagram the parent blue cube produces a child, the purple cube.
![IMG_0911](https://user-images.githubusercontent.com/11809261/225109770-666829ac-e54c-478d-a4ef-6d40c527cbf6.PNG)

The purple cube ended the simulation closer to the yellow goal than the blue cube. Thus, it has a better fitness score. The blue cube is deleted and the purple cube becomes the parent for the next generation.
![IMG_0912](https://user-images.githubusercontent.com/11809261/225109901-099c0e84-74f8-4665-aac7-6b37ef15b8b0.PNG)

## Fitness Values at each Generation
The following graph contains the best fitness value at each generation for 10 robots over 500 generations, with a population size of 10. A smaller fitness value was preferred. <img width="674" alt="Screen Shot 2023-03-14 at 9 51 32 PM" src="https://user-images.githubusercontent.com/11809261/225192917-91e7d441-76e2-4601-957c-7c0dad1998ec.png">

As evident from the graph, the rate of improvement starts out very steep, with robots improving almost every generation. As the robots become better and better, the improvement per generation becomes smaller and the generations which do improve become more sparse. This is typical of evolution - when robots have a very poor fitness, any change is somewhat likely to be beneficial. As the robots' become more and more fit, large changes become more likely to be harmful, because the robot is already nearing a local optimum in terms of fitness. However, this form of evolution only excels at finding local optima. These robots may not, and in fact are clearly not, the optimal solution to reach the point -100, -100. More optimal robots could be found by increasing genetic diversity in the robots early on. This can be accomplished by using evolutionary algorithms other than the parallel hill climber.

Another reason for this dropoff is the brain-body mutation algorithm. The algorithm mutates the body more often early in the evolutionary process, and gradually becomes less likely to mutate the body and more likely to mutate the brain. This reduces the diversity of the population but allows for optimizing the body type the robot found by the middle generations. The thought process behind this choice was that by the middle generations, the robots are already approaching a local optimum. Doing large changes on the robot, such as changing its body, would be more likely to harm the robot's fitness than help. Thus, we make small changes towards the end of the algorithm.

# Citations
Code for this reposity is based on the following:

[ludobots](https://www.reddit.com/r/ludobots/)

[pybullet](https://pybullet.org/wordpress/)

[pyrosim](https://github.com/ccappelle/pyrosim)
