import pybullet as p
import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c
import math

class SOLUTION:

    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.sensorIDs = []
        # self.numLinks = random.randint(c.minLinks, c.maxLinks)
        self.weights = []
        self.nextLinkID = 0
        self.joints = []
        # Keep track of the space that current links occupy. 3 dimensional array - links, dimensions, space occipied
        self.occupiedSpace = []
        # Keep track of the absolute position of the last joint
        self.lastAbsolutePos = {}

    def Evaluate(self, directOrGUI):
        pass
        # self.Create_World()
        # self.Create_Body()
        # self.Create_Brain()
        # os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " &")
        # while not os.path.exists("fitness" + str(self.myID) + ".txt"):
        #     time.sleep(0.01)
        # f = open("fitness" + str(self.myID) + ".txt", "r")
        # self.fitness = float(f.read())
        # f.close()

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        # os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " 2&>1 &")
        os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " &")

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.01)
        f = open("fitness" + str(self.myID) + ".txt", "r")
        self.fitness = float(f.read())
        f.close()
        os.system("rm fitness" + str(self.myID) + ".txt")        

    def Mutate(self):
        print("Sensors: ")
        print(self.sensorIDs)

        row = random.randint(0, c.numHiddenNeurons - 1)
        column = self.sensorIDs.index(random.choice(self.sensorIDs))

        self.weights[0][row][column] = random.random() * 2 - 1

        column = random.randint(0, len(self.joints))
        self.weights[1][row][column] = random.random() * 2 - 1

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID

    def Create_World(self):

        length = 1
        width = 1
        height = 3

        x = -100
        y = -100
        z = height/2

        pyrosim.Start_SDF("world.sdf")

        pyrosim.Send_Cube(name="Box1", pos=[x, y, z], size=[length, width, height])

        x = -105
        y = -105
        pyrosim.Send_Cube(name="Box2", pos=[x, y, z], size=[length, width, height])

        pyrosim.End()


    def Create_Body(self):
        # length = random.randint(1, 20) / 20
        # width = random.randint(1, 20) / 20
        # height = random.randint(1, 20) / 20

        # prevLength = length
        # prevWidth = width
        # prevHeight = height
        
        size = [x / 10 for x in random.sample(range(1, 20), 3)]
        pos = [0, 0, 1]

        pyrosim.Start_URDF("body.urdf")

        self.sensorIDs = []

        if random.random() < 0.5:
            pyrosim.Send_Cube(name = "0", pos = [0, 0, 1], size = size, colorName = 'green')
            self.sensorIDs.append(0)
        else:
            pyrosim.Send_Cube(name = "0", pos = [0, 0, 1], size = size, colorName = 'blue')
        
        self.lastAbsolutePos[0] = [0, 0, 0]
        # Update the space that the links occupy
        space = []
        for axis in range(0, len(size)):
            min = pos[axis] - abs(size[axis] / 2)
            max = pos[axis] + abs(size[axis] / 2)
            space.append([min, max])
        self.occupiedSpace.append(space)

        self.nextLinkID += 1

        # Don't let the robot go in the -z direction, so don't include -3 in directions
        self.Create_Link_Tree(0, 1, [-2, -1, 1, 2, 3], size, 3)


        # pyrosim.Send_Cube(name = "0", pos = [0, 0, 1], size = size)
        # for id in range(0, self.numLinks):
        #     pos = size
        #     # size = random.sample(range(0.1, 2), 3)
        #     size = [x / 10 for x in random.sample(range(1, 20), 3)]

        #     print(size)              

        pyrosim.End()

    # Recursivley create links. Keep track of the direction that the link 'trees' have taken from the origin. They cannot go back in the same direction
    # (turn back on themselves). Keep going until a certain depth is reached

    def Create_Link_Tree(self, parentID, depth, availableDirections, prevSize, prevDirection):
        directions = availableDirections.copy()
        size = [x / 10 for x in random.sample(range(1, 20), 3)]
        direction = random.choice(directions)
        pos = [0, 0, 0]

        # While size is within position from previous links, shrink link

        # Shift the block from joint in the direction chosen. Multiply size by -1 if direction is negative
        pos[abs(direction) - 1] = size[abs(direction) - 1]/2 * (direction / abs(direction))

        jointPos = [0, 0, 0]
        if depth == 1:
            jointPos[2] = 1
            jointPos[abs(direction) - 1] += prevSize[abs(direction) - 1] / 2 * (direction / abs(direction))
        else:
            jointPos[abs(prevDirection) - 1] = prevSize[abs(prevDirection) - 1] / 2 * (prevDirection / abs(prevDirection))
            jointPos[abs(direction) - 1] += prevSize[abs(direction) - 1] / 2 * (direction / abs(direction))

        # Update the last position
        self.lastAbsolutePos[self.nextLinkID] = [0, 0, 0]
        for axis in range(0, len(jointPos)):
            self.lastAbsolutePos[self.nextLinkID][axis] = self.lastAbsolutePos[parentID][axis] + jointPos[axis]

        pos, size = self.Check_For_Intersections(pos, size, direction)

        # Prevent the link tree from doubling back on itself
        if -1 * direction in directions:
            directions.remove(-1 * direction)

        # Last link in the tree. Base case.
        if depth == c.maxLinks:
            # If no links are sensor links, make end link a sensor. Otherwise, make the link a sensor 50% of the time
            if (random.random() < 0.5) or (len(self.sensorIDs) == 0):
                self.sensorIDs.append(self.nextLinkID)
                self.Create_Random_Link(parentID, self.nextLinkID, pos, size, 'green', jointPos)
            else:
                self.Create_Random_Link(parentID, self.nextLinkID, pos, size, 'blue', jointPos)
        else:
            if (random.random() < 0.5):
                self.Create_Random_Link(parentID, self.nextLinkID, pos, size, 'green', jointPos)
            else:
                self.Create_Random_Link(parentID, self.nextLinkID, pos, size, 'blue', jointPos)
            # 10% chance of ending the branch
            # if (random.random() < 0.1):
            #     return

            # numBranches = random.randint(1, len(directions) - 1)
            # spliceStart = 0
            # while spliceStart < len(directions):
            #     self.Create_Link_Tree(self.nextLinkID-1, depth + 1, directions[spliceStart:spliceStart + Math.floor(len(directions)/numBranches)], size, direction)
            self.Create_Link_Tree(self.nextLinkID-1, depth + 1, directions, size, direction)

        
    def Check_For_Intersections(self, pos, size, direction):
        for linkSpace in self.occupiedSpace:
            for axis in range(0, len(linkSpace)):
                dim1min = self.lastAbsolutePos[self.nextLinkID][axis] + pos[axis] - abs(size[axis] / 2)
                dim1max = self.lastAbsolutePos[self.nextLinkID][axis] + pos[axis] + abs(size[axis] / 2)
                dim2min = self.lastAbsolutePos[self.nextLinkID][(axis + 1) % 3] + pos[(axis + 1) % 3] - abs(size[(axis + 1) % 3] / 2)
                dim2max = self.lastAbsolutePos[self.nextLinkID][(axis + 1) % 3] + pos[(axis + 1) % 3] + abs(size[(axis + 1) % 3] / 2)
                dim3min = self.lastAbsolutePos[self.nextLinkID][(axis + 2) % 3] + pos[(axis + 2) % 3] - abs(size[(axis + 2) % 3] / 2)
                dim3max = self.lastAbsolutePos[self.nextLinkID][(axis + 2) % 3] + pos[(axis + 2) % 3] + abs(size[(axis + 2) % 3] / 2)
                print('axis:' + str(axis))
                print('axis + 1:' + str((axis + 1) % 3))
                print('axis + 1 last pos value:' + str(self.lastAbsolutePos[self.nextLinkID][(axis + 1) % 3]))
                # Give 0.1 margin because of rounding
                while (((linkSpace[axis][0]+0.01) < dim1min < (linkSpace[axis][1]-0.01)) or 
                    ((linkSpace[axis][0]+0.01) < dim1max < (linkSpace[axis][1]-0.01))):
                    print("Dim 1 check passed")
                    if ((linkSpace[(axis + 1) % 3][0]+0.01 < dim2min < linkSpace[(axis + 1) % 3][1]-0.01) or 
                        (linkSpace[(axis + 1) % 3][0]+0.01 < dim2max < linkSpace[(axis + 1) % 3][1]-0.01)):
                        print("Dim 2 check passed")
                        if ((linkSpace[(axis + 2) % 3][0]+0.01 < dim3min < linkSpace[(axis + 2) % 3][1]-0.01) or 
                            (linkSpace[(axis + 2) % 3][0]+0.01 < dim3max < linkSpace[(axis + 2) % 3][1]-0.01)):
                            ("Dim 3 check passed")

                            dimensionToChange = random.randint(0, 2)
                            size[dimensionToChange] -= 0.05
                            print("Dimension: " + str(dimensionToChange) + "Size: " + str(size[dimensionToChange]))
                            if (dimensionToChange == abs(direction) - 1):
                                pos[abs(direction) - 1] = size[abs(direction) - 1]/2 * (direction / abs(direction))
                            dim1min = self.lastAbsolutePos[self.nextLinkID][axis] + pos[axis] - abs(size[axis] / 2)
                            dim1max = self.lastAbsolutePos[self.nextLinkID][axis] + pos[axis] + abs(size[axis] / 2)
                            dim2min = self.lastAbsolutePos[self.nextLinkID][(axis + 1) % 3] + pos[(axis + 1) % 3] - abs(size[(axis + 1) % 3] / 2)
                            dim2max = self.lastAbsolutePos[self.nextLinkID][(axis + 1) % 3] + pos[(axis + 1) % 3] + abs(size[(axis + 1) % 3] / 2)
                            dim3min = self.lastAbsolutePos[self.nextLinkID][(axis + 2) % 3] + pos[(axis + 2) % 3] - abs(size[(axis + 1) % 3] / 2)
                            dim3max = self.lastAbsolutePos[self.nextLinkID][(axis + 2) % 3] + pos[(axis + 2) % 3] + abs(size[(axis + 1) % 3] / 2)
                        else:
                            break
                    else:
                        break
        return pos, size

    # Creates a random link with id childID. Also creates a joint from parentID to childID.
    def Create_Random_Link(self, parentID, childID, pos, size, colorName, jointPos):
        if parentID == 0:
            pyrosim.Send_Cube(name=str(childID), pos=pos, size=size, colorName = colorName)
            pyrosim.Send_Joint(name = str(parentID) + "_" + str(childID) , parent= str(parentID) , child = str(childID) , type = "revolute", position = jointPos, jointAxis = "1 1 0")
        else:
            pyrosim.Send_Cube(name=str(childID), pos=pos, size=size, colorName = colorName)
            pyrosim.Send_Joint(name = str(parentID) + "_" + str(childID) , parent= str(parentID) , child = str(childID) , type = "revolute", position = jointPos, jointAxis = "1 1 0")

        # Update the space that the links occupy
        space = []
        for axis in range(0, len(size)):
            min = self.lastAbsolutePos[self.nextLinkID][axis] + pos[axis] - abs(size[axis] / 2)
            max = self.lastAbsolutePos[self.nextLinkID][axis] + pos[axis] + abs(size[axis] / 2)
            space.append([min, max])
        self.occupiedSpace.append(space)

        self.joints.append([parentID, childID])
        self.nextLinkID += 1

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        # pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "BackLowerLeg")
        # pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "FrontLowerLeg")
        # pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "LeftLowerLeg")
        # pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "RightLowerLeg")
        
        # Could also be replaced with a random number of hidden neurons
        numHiddenNeurons = c.numHiddenNeurons

        # for id in range(0, self.nextLinkID):
        #     if id in self.sensorIDs:
        #         # Number of motor joints = self.numLinks-1, ids start at 0
        #         pyrosim.Send_Sensor_Neuron(name = self.sensorIDs.index(id) + (self.numLinks-1) + numHiddenNeurons , linkName = str(id))
            # if not id == self.numLinks - 1:
            #     pyrosim.Send_Motor_Neuron( name = id , jointName = str(id) + "_" + str(id + 1))

        for id in self.sensorIDs:
            pyrosim.Send_Sensor_Neuron(name = self.sensorIDs.index(id) + len(self.joints) + numHiddenNeurons , linkName = str(id))            

        for joint in self.joints:
            pyrosim.Send_Motor_Neuron( name = self.joints.index(joint) , jointName = str(joint[0]) + "_" + str(joint[1]))


        # pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_BackLeg")
        # pyrosim.Send_Motor_Neuron( name = 5 , jointName = "Torso_FrontLeg")
        # pyrosim.Send_Motor_Neuron( name = 6 , jointName = "Torso_LeftLeg")
        # pyrosim.Send_Motor_Neuron( name = 7 , jointName = "Torso_RightLeg")
        # pyrosim.Send_Motor_Neuron( name = 8 , jointName = "BackLeg_BackLowerLeg")
        # pyrosim.Send_Motor_Neuron( name = 9 , jointName = "FrontLeg_FrontLowerLeg")
        # pyrosim.Send_Motor_Neuron( name = 10 , jointName = "LeftLeg_LeftLowerLeg")
        # pyrosim.Send_Motor_Neuron( name = 11 , jointName = "RightLeg_RightLowerLeg")

        # pyrosim.Send_Hidden_Neuron(name = 12)
        # pyrosim.Send_Hidden_Neuron(name = 13)
        # pyrosim.Send_Hidden_Neuron(name = 14)
        # pyrosim.Send_Hidden_Neuron(name = 15)

        for hiddenNeuronID in range(0, numHiddenNeurons):
            pyrosim.Send_Hidden_Neuron(name = len(self.joints) + hiddenNeuronID)


        # pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 3 , weight = -1.0 )
        # pyrosim.Send_Synapse( sourceNeuronName = 1 , targetNeuronName = 3 , weight = -1.0 )
        # pyrosim.Send_Synapse( sourceNeuronName = 2 , targetNeuronName = 4 , weight = 1.0 )

        self.weights = [np.random.rand(numHiddenNeurons, len(self.sensorIDs)), np.random.rand(numHiddenNeurons, len(self.joints))]
        self.weights[0] = self.weights[0] * 2 - 1
        self.weights[1] = self.weights[1] * 2 - 1

        for currentRow in range(0, numHiddenNeurons):
            for currentColumn in range(0, len(self.sensorIDs)):
                    sensorName = currentColumn + len(self.joints) + numHiddenNeurons
                    hiddenNeuronName = len(self.joints) + currentRow
                    pyrosim.Send_Synapse( sourceNeuronName = sensorName , targetNeuronName = hiddenNeuronName , weight = self.weights[0][currentRow][currentColumn] )

        for currentRow in range(0, numHiddenNeurons):
            for currentColumn in range(0, len(self.joints)):
                    motorName = currentColumn
                    hiddenNeuronName = len(self.joints) + currentRow
                    pyrosim.Send_Synapse( sourceNeuronName = hiddenNeuronName , targetNeuronName = motorName , weight = self.weights[1][currentRow][currentColumn] )


        pyrosim.End()