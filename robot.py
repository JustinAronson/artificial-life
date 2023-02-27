import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c

class ROBOT:

    def __init__(self, solutionID):
        self.robot = p.loadURDF("body" + solutionID + ".urdf")
        os.system("rm body" + str(solutionID) + ".urdf")
        pyrosim.Prepare_To_Simulate(self.robot)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.nn = NEURAL_NETWORK("brain" + solutionID + ".nndf")
        # os.system("rm brain" + str(solutionID) + ".nndf")
        self.solutionID = solutionID
        self.robotPositionDifference = 200
        self.boxPositionDifference = 200

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, t):
        for sensor in self.sensors:
            self.sensors[sensor].Get_Value(t)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                desiredAngle *= c.motorJointRange
                # self.motors[bytes(jointName, 'utf-8')].Set_Value(self.robot, desiredAngle)  
                self.motors[jointName].Set_Value(self.robot, desiredAngle)

    def Think(self):
        try:
            self.nn.Update()
        except:
            print('Error updating the neural network.')
            print('Brain ID: ' + str(self.solutionID))

    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.robot, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]
        f = open("tmp" + str(self.solutionID) + ".txt", "w")
        # f.write(str(self.robotPositionDifference + self.boxPositionDifference*4))
        f.write(str(self.robotPositionDifference))
        f.close()

        os.system("mv tmp" + str(self.solutionID) + ".txt fitness" + str(self.solutionID) + ".txt")

    def Find_Fitness(self, bottomBoxPos, topBoxPos):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robot)
        basePosition = basePositionAndOrientation[0]

        bottomPos = bottomBoxPos[0]
        topPos = topBoxPos[0]
        xDistance = basePosition[0] - topPos[0]
        yDistance = basePosition[1] - topPos[1]
        zDistance = basePosition[2] - topPos[2]
        robotPositionDifference = (xDistance**2 + yDistance**2 + zDistance**2)**0.5

        if robotPositionDifference < self.robotPositionDifference:
            self.robotPositionDifference = robotPositionDifference

        xDistance = bottomPos[0] - topPos[0]
        yDistance = bottomPos[1] - topPos[1]
        zDistance = bottomPos[2] + 1 - topPos[2]
        boxPositionDifference = (xDistance**2 + yDistance**2 + zDistance**2)**0.5

        if boxPositionDifference < self.boxPositionDifference:
            self.boxPositionDifference = boxPositionDifference

        pass