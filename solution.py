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
        self.sensors = []
        # self.numLinks = random.randint(c.minLinks, c.maxLinks)
        self.nextLinkID = 0
        self.joints = []
        # Keep track of the space that current links occupy. 3 dimensional array - links, dimensions, space occipied
        self.occupiedSpace = []
        # Keep track of the absolute position of the last joint
        self.lastAbsolutePos = {}
        # Create body plan
        # Format: array of links. Each link is an array of: ID, parentID, pos, size, colorName, availableDirections, direction
        self.linkPlan = []
        # Format: array of joints. Each joint is an array of: parentID, childID, pos
        self.jointPlan = []

        # Keep track of all link data. Format:
        # Format: key: link. Value: [parentID, depth, availableDirections, prevSize, prevDirection]
        self.links = {}
        # Could also be replaced with a random number of hidden neurons
        self.numHiddenNeurons = c.numHiddenNeurons

        # Called on the first generation of robots.
        self.Create_Body_Plan()

        # self.weights = [np.random.rand(self.numHiddenNeurons, len(self.sensors)), np.random.rand(self.numHiddenNeurons, len(self.joints))]
        # self.weights[0] = self.weights[0] * 2 - 1
        # self.weights[1] = self.weights[1] * 2 - 1

        # print('Sensor shape: ')
        # print(self.weights[0].shape)
        # print('Motor shape: ')
        # print(self.weights[1].shape)
        # print('')

        self.sensorWeights = {}
        self.motorWeights = {}



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
        os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " 2&>1 &")
        # os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " &")
        # os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID))

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.01)
        f = open("fitness" + str(self.myID) + ".txt", "r")
        self.fitness = float(f.read())
        f.close()
        os.system("rm fitness" + str(self.myID) + ".txt")        

    def Mutate(self):
        # print("Sensors: ")
        # print(self.sensors)
        if random.random() < 0.3:
            self.Mutate_Body()
        else:
            self.Mutate_Brain()

    def Mutate_Brain(self):
        sensorToChange = random.choice(self.sensors)
        self.sensorWeights[sensorToChange][random.randint(0, self.numHiddenNeurons - 1)] = random.random() * 2 - 1

        motorToChange = random.choice(self.jointPlan)
        self.motorWeights[self.jointPlan.index(motorToChange)][random.randint(0, self.numHiddenNeurons - 1)] = random.random() * 2 - 1

        mutationProbability = random.random()
        # Add or subtract a hidden neuron with 10% likelihood
        if mutationProbability < 0.1:
            self.numHiddenNeurons += 1
        elif mutationProbability < 0.2:
            if self.numHiddenNeurons > 1:
                self.numHiddenNeurons -= 1

    def Mutate_Body(self):
        mutationProbability = random.random()
        # 10% chance to add links
        if mutationProbability < 0.1:
            self.Add_Links()

        # 10% to remove links
        elif mutationProbability < 0.2:
            # If there two or fewer links, do not remove
            if len(self.linkPlan) > 2:
                # print('Going into remove links')
                self.Remove_Links()

        # 20% chance to add sensor link
        elif mutationProbability < 0.4:
            # print('Adding sensor')
            self.Switch_Sensor_Status('blue', 'green')

        # 20% chance to remove a sensor link
        elif mutationProbability < 0.6:
            # print('Removing sensor')
            self.Switch_Sensor_Status('green', 'blue')

    def Switch_Sensor_Status(self, currentColor, newColor):
        swappableLinks = []
        linkIndex = 0
        while linkIndex < len(self.linkPlan):
            if self.linkPlan[linkIndex][4] == currentColor:
                swappableLinks.append(linkIndex)
            linkIndex += 1

        if len(swappableLinks) > 0:
            linkToChange = random.choice(swappableLinks)
            self.linkPlan[linkToChange][4] = newColor        
            
    def Remove_Links(self):
        # Remove one link
        linksWithoutChildren = []
        for link in self.linkPlan:
            hasChildren = False
            for child in self.linkPlan:
                if child[1] == link[0]:
                    hasChildren = True
                    break
            if not hasChildren:
                linksWithoutChildren.append(link)

        # If there are no links without children, return (should never happen)
        if len(linksWithoutChildren) == 0:
            return

        # parent = []
        # for link in self.linkPlan:
        #     if link[0] == linkToRemove[1]:
        #         parent = link

        linkToRemove = random.choice(linksWithoutChildren)
        # print('Removing link :')
        # print(linkToRemove)

        self.linkPlan.remove(linkToRemove)

        for joint in self.jointPlan:
            # if joint[0] == parent[0] and joint[1] == linkToRemove[0]:
            if joint[1] == linkToRemove[0]:
                # print('Removing joint : ')
                # print(joint)
                # Remove the joint from weights
                del self.motorWeights[self.jointPlan.index(joint)]

                self.jointPlan.remove(joint)

    # Mutation to add links to creature
    def Add_Links(self):
        mutationProbability = random.random()
        numToAdd = 0
        # Add one link
        if mutationProbability < 0.6:
            numToAdd = 1
        # Add two links
        elif mutationProbability < 0.9:
            numToAdd = 2
        # Add three links
        else:
            numToAdd = 3
        linkToAdd = random.choice(self.linkPlan)

        # Choose a link with open faces. This will never become an infinite loop because
        # there will always be a link at the end of the tree
        while len(linkToAdd[5]) == 0:
            linkToAdd = random.choice(self.linkPlan)

        self.Create_Link_Tree(linkToAdd[0], c.maxDepth - numToAdd, linkToAdd[5], linkToAdd[3], linkToAdd[6])

    # Mutation to change a link's size
    def Change_Link_Size(self):
        linkToChange = random.choice(self.linkPlan)
        

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
        pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")
        #pyrosim.Start_URDF("body.urdf")
             
        self.Create_Links()

        pyrosim.End()

    def Create_Body_Plan(self):
        size = [x / 10 for x in random.sample(range(1, 20), 3)]
        pos = [0, 0, 1]

        self.sensorIDs = []

        if random.random() < 0.5:
            # pyrosim.Send_Cube(name = "0", pos = [0, 0, 1], size = size, colorName = 'green')
            self.linkPlan.append([0, None, pos, size, 'green', [-2, -1, 1, 2, 3], None])
            self.sensorIDs.append(0)
        else:
            # pyrosim.Send_Cube(name = "0", pos = [0, 0, 1], size = size, colorName = 'blue')
            self.linkPlan.append([0, None, pos, size, 'blue', [-2, -1, 1, 2, 3], None])
        
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

        self.sensors = []
        for link in self.linkPlan:
            if link[4] == 'green':
                self.sensors.append(link[0])       


    # Recursivley create links. Keep track of the direction that the link 'trees' have taken from the origin. They cannot go back in the same direction
    # (turn back on themselves). Keep going until a certain depth is reached
    def Create_Link_Tree(self, parentID, depth, availableDirections, prevSize, prevDirection):
        # print("In Create_Link_Tree, depth = " + str(depth))
        pos, size, direction, directions, jointPos, noSpaceFlag = self.Set_Link_Stats(parentID, availableDirections, prevSize, prevDirection)
        if noSpaceFlag:
            return

        # If no links are sensor links, make end link a sensor. Otherwise, make the link a sensor 50% of the time   
        if (random.random() < 0.5) or (depth == c.maxDepth and (len(self.sensorIDs) == 0)):
            # self.Create_Random_Link(parentID, self.nextLinkID, pos, size, 'green', jointPos)
            self.linkPlan.append([self.nextLinkID, parentID, pos, size, 'green', directions, direction])
        else:
            # self.Create_Random_Link(parentID, self.nextLinkID, pos, size, 'blue', jointPos)
            self.linkPlan.append([self.nextLinkID, parentID, pos, size, 'blue', directions, direction])


        self.jointPlan.append([parentID, self.nextLinkID, jointPos])

        # Update the space that the links occupy
        space = []
        for axis in range(0, len(size)):
            min = self.lastAbsolutePos[self.nextLinkID][axis] + pos[axis] - abs(size[axis] / 2)
            max = self.lastAbsolutePos[self.nextLinkID][axis] + pos[axis] + abs(size[axis] / 2)
            space.append([min, max])
        self.occupiedSpace.append(space)

        # self.joints.append([parentID, self.nextLinkID])

        # Update available directions for parent
        for link in self.linkPlan:
            if link[0] == parentID:
                link[5].remove(direction)

        self.nextLinkID += 1

        # Last link in the tree is base case.
        if depth < c.maxDepth:
            linkID = self.nextLinkID-1

            if len(directions) == 1:
                self.Create_Link_Tree(linkID, depth + 1, directions, size, direction)
            else:
                numBranches = random.randint(1, len(directions) - 1)
                increment = math.floor(len(directions)/numBranches)
                spliceStart = 0
                if increment == 0:
                    increment += 1
                end = len(directions)
                while spliceStart < end:
                    if spliceStart + increment <= len(directions):
                        self.Create_Link_Tree(linkID, depth + 1, directions[spliceStart:spliceStart + math.floor(len(directions)/numBranches)], size, direction)
                    else:
                        self.Create_Link_Tree(linkID, depth + 1, directions[spliceStart:], size, direction)
                    spliceStart += increment

            # self.Create_Link_Tree(self.nextLinkID-1, depth + 1, directions, size, direction)

    def Set_Link_Stats(self, parentID, availableDirections, prevSize, prevDirection):
        directions = availableDirections.copy()
        size = [random.randrange(1, 5), random.randrange(1, 5), random.randrange(1, 5)]
        if len(directions) == 0:
            noSpaceFlag = True
            return None, None, None, None, None, noSpaceFlag
        direction = random.choice(directions)
        pos = [0, 0, 0]

        # While size is within position from previous links, shrink link

        # Shift the block from joint in the direction chosen. Multiply size by -1 if direction is negative
        pos[abs(direction) - 1] = size[abs(direction) - 1]/2 * (direction / abs(direction))

        jointPos = [0, 0, 0]
        if parentID == 0:
            jointPos[2] = 1
            jointPos[abs(direction) - 1] += self.linkPlan[0][3][abs(direction) - 1] / 2 * (direction / abs(direction))
        else:
            jointPos[abs(prevDirection) - 1] = prevSize[abs(prevDirection) - 1] / 2 * (prevDirection / abs(prevDirection))
            jointPos[abs(direction) - 1] += prevSize[abs(direction) - 1] / 2 * (direction / abs(direction))

        # Update the last position
        self.lastAbsolutePos[self.nextLinkID] = [0, 0, 0]
        for axis in range(0, len(jointPos)):
            self.lastAbsolutePos[self.nextLinkID][axis] = self.lastAbsolutePos[parentID][axis] + jointPos[axis]

        pos, size, noSpaceFlag = self.Check_For_Intersections(pos, size, direction)

        # Prevent the link tree from doubling back on itself
        if (-1 * direction in directions) and (not noSpaceFlag):
            directions.remove(-1 * direction)

        return pos, size, direction, directions, jointPos, noSpaceFlag

    def Check_For_Intersections(self, pos, size, direction):
        noSpaceFlag = False
        for linkSpace in self.occupiedSpace:
            for axis in range(0, len(linkSpace)):
                dim1min = self.lastAbsolutePos[self.nextLinkID][axis] + pos[axis] - abs(size[axis] / 2)
                dim1max = self.lastAbsolutePos[self.nextLinkID][axis] + pos[axis] + abs(size[axis] / 2)
                dim2min = self.lastAbsolutePos[self.nextLinkID][(axis + 1) % 3] + pos[(axis + 1) % 3] - abs(size[(axis + 1) % 3] / 2)
                dim2max = self.lastAbsolutePos[self.nextLinkID][(axis + 1) % 3] + pos[(axis + 1) % 3] + abs(size[(axis + 1) % 3] / 2)
                dim3min = self.lastAbsolutePos[self.nextLinkID][(axis + 2) % 3] + pos[(axis + 2) % 3] - abs(size[(axis + 2) % 3] / 2)
                dim3max = self.lastAbsolutePos[self.nextLinkID][(axis + 2) % 3] + pos[(axis + 2) % 3] + abs(size[(axis + 2) % 3] / 2)
                # print('axis:' + str(axis))
                # print('axis + 1:' + str((axis + 1) % 3))
                # print('axis + 1 last pos value:' + str(self.lastAbsolutePos[self.nextLinkID][(axis + 1) % 3]))
                # Give 0.1 margin because of rounding
                while (((linkSpace[axis][0]+0.01) < dim1min < (linkSpace[axis][1]-0.01)) or 
                    ((linkSpace[axis][0]+0.01) < dim1max < (linkSpace[axis][1]-0.01))) or ((linkSpace[axis][0]+0.01) > dim1min
                    and dim1max > (linkSpace[axis][1]-0.01)):
                    # print("Dim 1 check passed")
                    if ((linkSpace[(axis + 1) % 3][0]+0.01 < dim2min < linkSpace[(axis + 1) % 3][1]-0.01) or 
                        (linkSpace[(axis + 1) % 3][0]+0.01 < dim2max < linkSpace[(axis + 1) % 3][1]-0.01)) or ((linkSpace[(axis + 1) % 3][0]+0.01) > dim2min
                        and dim2max > (linkSpace[(axis + 1) % 3][1]-0.01)):
                        # print("Dim 2 check passed")
                        if ((linkSpace[(axis + 2) % 3][0]+0.01 < dim3min < linkSpace[(axis + 2) % 3][1]-0.01) or 
                            (linkSpace[(axis + 2) % 3][0]+0.01 < dim3max < linkSpace[(axis + 2) % 3][1]-0.01)) or ((linkSpace[(axis + 2) % 3][0]+0.01) > dim3min
                            and dim3max > (linkSpace[(axis + 2) % 3][1]-0.01)):
                            # print("No space")

                            noSpaceFlag = True
                            break
                            # dimensionToChange = 0
                            # if size[dimensionToChange] < 0.2:
                            #     dimensionToChange = 1
                            #     if size[dimensionToChange] < 0.2:
                            #         dimensionToChange = 2
                            #         if size[dimensionToChange] < 0.2:
                            #             print('All dimensions small')
                            #             noSpaceFlag = True
                            #             break
                            # size[dimensionToChange] -= 0.05
                            # # print("Dimension: " + str(dimensionToChange) + "Size: " + str(size[dimensionToChange]))
                            # if (dimensionToChange == abs(direction) - 1):
                            #     pos[abs(direction) - 1] = size[abs(direction) - 1]/2 * (direction / abs(direction))
                            # dim1min = self.lastAbsolutePos[self.nextLinkID][axis] + pos[axis] - abs(size[axis] / 2)
                            # dim1max = self.lastAbsolutePos[self.nextLinkID][axis] + pos[axis] + abs(size[axis] / 2)
                            # dim2min = self.lastAbsolutePos[self.nextLinkID][(axis + 1) % 3] + pos[(axis + 1) % 3] - abs(size[(axis + 1) % 3] / 2)
                            # dim2max = self.lastAbsolutePos[self.nextLinkID][(axis + 1) % 3] + pos[(axis + 1) % 3] + abs(size[(axis + 1) % 3] / 2)
                            # dim3min = self.lastAbsolutePos[self.nextLinkID][(axis + 2) % 3] + pos[(axis + 2) % 3] - abs(size[(axis + 2) % 3] / 2)
                            # dim3max = self.lastAbsolutePos[self.nextLinkID][(axis + 2) % 3] + pos[(axis + 2) % 3] + abs(size[(axis + 2) % 3] / 2)
                        else:
                            break
                    else:
                        break
        return pos, size, noSpaceFlag

    # Creates a random link with id childID. Also creates a joint from parentID to childID.
    def Create_Links(self):
        for link in self.linkPlan:
            pyrosim.Send_Cube(name=str(link[0]), pos=link[2], size=link[3], colorName = link[4])
        for joint in self.jointPlan:
            pyrosim.Send_Joint(name = str(joint[0]) + "_" + str(joint[1]) , parent= str(joint[0]) , child = str(joint[1]) , type = "revolute", position = joint[2], jointAxis = "1 1 0")

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        sensorIndex = 0
        self.sensors = []
        for link in self.linkPlan:
            if link[4] == 'green':
                pyrosim.Send_Sensor_Neuron(name = sensorIndex + len(self.jointPlan) + self.numHiddenNeurons , linkName = str(link[0]))
                # self.sensors.append(link[0])       
                # sensorIndex += 1
                if link[0] not in self.sensorWeights:
                    self.sensorWeights[link[0]] = []
                    for i in range(0, self.numHiddenNeurons):
                        self.sensorWeights[link[0]].append(random.random() * 2 - 1)

                for i in range(0, self.numHiddenNeurons):
                    hiddenNeuronName = len(self.jointPlan) + i
                    pyrosim.Send_Synapse( sourceNeuronName = sensorIndex + len(self.jointPlan) + self.numHiddenNeurons , targetNeuronName = hiddenNeuronName , weight = self.sensorWeights[link[0]][i] )

                self.sensors.append(link[0])     
                sensorIndex += 1
            
        # print("Sensors: ")
        # print(self.sensors)

        for joint in self.jointPlan:
            pyrosim.Send_Motor_Neuron( name = self.jointPlan.index(joint) , jointName = str(joint[0]) + "_" + str(joint[1]))

            # Will need to be changed if deleting links for evolution
            if self.jointPlan.index(joint) not in self.motorWeights:
                self.motorWeights[self.jointPlan.index(joint)] = []
                for i in range(0, self.numHiddenNeurons):
                    self.motorWeights[self.jointPlan.index(joint)].append(random.random() * 2 - 1)

            for i in range(0, self.numHiddenNeurons):
                hiddenNeuronName = len(self.jointPlan) + i
                pyrosim.Send_Synapse( sourceNeuronName = hiddenNeuronName , targetNeuronName = self.jointPlan.index(joint) , weight = self.motorWeights[self.jointPlan.index(joint)][i] )

        for hiddenNeuronID in range(0, self.numHiddenNeurons):
            pyrosim.Send_Hidden_Neuron(name = len(self.jointPlan) + hiddenNeuronID)

        pyrosim.End()