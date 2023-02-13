import pybullet as p
import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c

class SOLUTION:

    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.sensorIDs = []
        self.numLinks = random.randint(2, 4)
        self.weights = []

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

        column = random.randint(0, self.numLinks - 1)
        self.weights[1][row][column] = random.random() * 2 - 1

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID

    def Create_World(self):

        length = 1
        width = 1
        height = 3

        x = -4
        y = -4
        z = height/2

        pyrosim.Start_SDF("world.sdf")

        pyrosim.Send_Cube(name="Box1", pos=[x, y, z], size=[length, width, height])

        x = -1
        y = -2
        pyrosim.Send_Cube(name="Box2", pos=[x, y, z], size=[length, width, height])

        pyrosim.End()


    def Create_Body(self):
        # length = random.randint(1, 20) / 20
        # width = random.randint(1, 20) / 20
        # height = random.randint(1, 20) / 20

        # prevLength = length
        # prevWidth = width
        # prevHeight = height
        
        # Starting size will be reset, this is for position of the robot
        size = [0, 0, 1]

        pyrosim.Start_URDF("body.urdf")

        self.sensorIDs = []

        # pyrosim.Send_Cube(name = "0", pos = [0, 0, 1], size = size)
        for id in range(0, self.numLinks):
            pos = size
            # size = random.sample(range(0.1, 2), 3)
            size = [x / 10 for x in random.sample(range(1, 20), 3)]

            print(size)

            # Make a link a sensor 50% of the time. If no links are sensor links, make the last link a sensor
            if (random.random() < 0.5) or (id == self.numLinks-1 and len(self.sensorIDs) == 0):
                self.sensorIDs.append(id)
                self.Create_Random_Link(id, pos, size, id == self.numLinks-1, 'green')
            else:
                self.Create_Random_Link(id, pos, size, id == self.numLinks-1, 'blue')                

        pyrosim.End()

    def Create_Random_Link(self, id, pos, size, endFlag, colorName):
        pyrosim.Send_Cube(name=str(id), pos=[x / 2 for x in size], size=size, colorName = colorName)
        if id == 0:
            pyrosim.Send_Joint(name = str(id) + "_" + str(id+1) , parent= str(id) , child = str(id+1) , type = "revolute", position = [size[0]/2, size[1]/2, size[2]/2 + 0.5], jointAxis = "1 0 0")
        elif not endFlag:
            pyrosim.Send_Joint(name = str(id) + "_" + str(id+1) , parent= str(id) , child = str(id+1) , type = "revolute", position = size, jointAxis = "1 0 0")

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        # pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "BackLowerLeg")
        # pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "FrontLowerLeg")
        # pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "LeftLowerLeg")
        # pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "RightLowerLeg")
        
        # Could also be replaced with a random number of hidden neurons
        numHiddenNeurons = c.numHiddenNeurons

        for id in range(0, self.numLinks):
            if id in self.sensorIDs:
                # Number of motor joints = self.numLinks-1, ids start at 0
                pyrosim.Send_Sensor_Neuron(name = self.sensorIDs.index(id) + (self.numLinks-1) + numHiddenNeurons , linkName = str(id))
            if not id == self.numLinks - 1:
                pyrosim.Send_Motor_Neuron( name = id , jointName = str(id) + "_" + str(id + 1))


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
            pyrosim.Send_Hidden_Neuron(name = self.numLinks-1 + hiddenNeuronID)


        # pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 3 , weight = -1.0 )
        # pyrosim.Send_Synapse( sourceNeuronName = 1 , targetNeuronName = 3 , weight = -1.0 )
        # pyrosim.Send_Synapse( sourceNeuronName = 2 , targetNeuronName = 4 , weight = 1.0 )

        self.weights = [np.random.rand(numHiddenNeurons, len(self.sensorIDs)), np.random.rand(numHiddenNeurons, self.numLinks)]
        self.weights[0] = self.weights[0] * 2 - 1
        self.weights[1] = self.weights[1] * 2 - 1

        for currentRow in range(0, numHiddenNeurons):
            for currentColumn in range(0, len(self.sensorIDs)):
                    sensorName = currentColumn + (self.numLinks-1) + numHiddenNeurons
                    hiddenNeuronName = self.numLinks-1 + currentRow
                    pyrosim.Send_Synapse( sourceNeuronName = sensorName , targetNeuronName = hiddenNeuronName , weight = self.weights[0][currentRow][currentColumn] )

        for currentRow in range(0, numHiddenNeurons):
            for currentColumn in range(0, self.numLinks-1):
                    motorName = currentColumn
                    hiddenNeuronName = self.numLinks-1 + currentRow
                    pyrosim.Send_Synapse( sourceNeuronName = hiddenNeuronName , targetNeuronName = motorName , weight = self.weights[1][currentRow][currentColumn] )


        pyrosim.End()