import pybullet as p
import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c

class SOLUTION:

    def __init__(self, nextAvailableID):
        self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons)
        self.weights = self.weights * 2 - 1
        self.myID = nextAvailableID

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

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.01)
        f = open("fitness" + str(self.myID) + ".txt", "r")
        self.fitness = float(f.read())
        f.close()
        os.system("rm fitness" + str(self.myID) + ".txt")        

    def Mutate(self):
        row = random.randint(0, c.numSensorNeurons - 1)
        column = random.randint(0, c.numMotorNeurons - 1)

        self.weights[row, column] = random.random() * 2 - 1

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID

    def Create_World(self):

        length = 1
        width = 1
        height = 3

        x = -6
        y = -6
        z = height/2

        pyrosim.Start_SDF("world.sdf")

        pyrosim.Send_Cube(name="Box1", pos=[x, y, z], size=[length, width, height])

        x = -2
        y = -2
        pyrosim.Send_Cube(name="Box2", pos=[x, y, z], size=[length, width, height])

        pyrosim.End()


    def Create_Body(self):
        length = 1
        width = 1
        height = 1

        x = 0
        y = 0
        z = height/2
        
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.4], size=[length, width, height])

        pyrosim.Send_Joint(name = "Torso_LeftLeg" , parent= "Torso" , child = "LeftLeg" , type = "revolute", position = [-0.5, 0, 0.9], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[0, -0.5, 0], size=[0.2, 1, 0.2])

        pyrosim.Send_Joint(name = "LeftLeg_LeftLowerLeg" , parent= "LeftLeg" , child = "LeftLowerLeg" , type = "revolute", position = [0, -1, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name = "LeftLowerLeg_LeftRoller" , parent= "LeftLowerLeg" , child = "LeftRoller" , type = "revolute", position = [0.1, 0, -0.9], jointAxis = "0 0 1")
        pyrosim.Send_Cube(name="LeftRoller", pos=[0.5, 0, 0], size=[1, 0.2, 0.2])        

        pyrosim.Send_Joint(name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , type = "revolute", position = [0.50,0,0.9], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0, 0.5, 0], size=[0.2, 1, 0.2])

        pyrosim.Send_Joint(name = "RightLeg_RightLowerLeg" , parent= "RightLeg" , child = "RightLowerLeg" , type = "revolute", position = [0, 1, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name = "RightLowerLeg_RightRoller" , parent= "RightLowerLeg" , child = "RightRoller" , type = "revolute", position = [-0.1, 0, -0.9], jointAxis = "0 0 1")
        pyrosim.Send_Cube(name="RightRoller", pos=[-0.5, 0, 0], size=[1, 0.2, 0.2])   

        pyrosim.Send_Joint(name = "Torso_LeftArm" , parent= "Torso" , child = "LeftArm" , type = "revolute", position = [-0.2,0.5,1.5], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftArm", pos=[-0.5, 0, 0], size=[1, 0.2, 0.2])

        # pyrosim.Send_Joint(name = "LeftLeg_LeftLowerLeg" , parent= "LeftLeg" , child = "LeftLowerLeg" , type = "revolute", position = [-1, 0, 0], jointAxis = "0 1 0")
        # pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name = "Torso_RightArm" , parent= "Torso" , child = "RightArm" , type = "revolute", position = [0.2,0.5,1.5], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightArm", pos=[0.5, 0, 0], size=[1, 0.2, 0.2])

        # pyrosim.Send_Joint(name = "RightLeg_RightLowerLeg" , parent= "RightLeg" , child = "RightLowerLeg" , type = "revolute", position = [1, 0, 0], jointAxis = "0 1 0")
        # pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "RightLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "LeftArm")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "RightArm")
        pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "LeftRoller")
        pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "RightRoller")        


        pyrosim.Send_Motor_Neuron( name = 6 , jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron( name = 7 , jointName = "Torso_RightLeg")
        pyrosim.Send_Motor_Neuron( name = 8 , jointName = "Torso_LeftArm")
        pyrosim.Send_Motor_Neuron( name = 9 , jointName = "Torso_RightArm")
        pyrosim.Send_Motor_Neuron( name = 10 , jointName = "LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 11 , jointName = "RightLeg_RightLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 12 , jointName = "LeftLowerLeg_LeftRoller")
        pyrosim.Send_Motor_Neuron( name = 13 , jointName = "RightLowerLeg_RightRoller")
        # pyrosim.Send_Motor_Neuron( name = 10 , jointName = "LeftArm_LeftLowerLeg")
        # pyrosim.Send_Motor_Neuron( name = 11 , jointName = "RightLeg_RightLowerLeg")


        # pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = 3 , weight = -1.0 )
        # pyrosim.Send_Synapse( sourceNeuronName = 1 , targetNeuronName = 3 , weight = -1.0 )
        # pyrosim.Send_Synapse( sourceNeuronName = 2 , targetNeuronName = 4 , weight = 1.0 )

        for currentRow in range(0, c.numSensorNeurons):
            for currentColumn in range(0, c.numMotorNeurons):
                    pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn + 6 , weight = self.weights[currentRow][currentColumn] )


        pyrosim.End()