import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c
import world

class ROBOT:

    def __init__(self, solutionID):
        self.robot = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robot)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.nn = NEURAL_NETWORK("brain" + solutionID + ".nndf")
        os.system("rm brain" + str(solutionID) + ".nndf")
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
                self.motors[bytes(jointName, 'utf-8')].Set_Value(self.robot, desiredAngle)  
                 

    def Think(self):
        self.nn.Update()

    def Get_Fitness(self):
        # basePositionAndOrientation = p.getBasePositionAndOrientation(self.robot)
        # basePosition = basePositionAndOrientation[0]
        # # xPosition = basePosition[0]
        # # yPosition = basePosition[1]
        # xDistance = basePosition[0] - topPos[0]
        # yDistance = basePosition[1] - topPos[1]
        # zDistance = basePosition[2] - topPos[2]
        # robotPositionDifference = (xDistance**2 + yDistance**2 + zDistance**2)**0.5

        # bottomPos = p.getBasePositionAndOrientation(self.objects[0])
        # topPos = p.getBasePositionAndOrientation(self.objects[1])
        # xDistance = bottomPos[0] - topPos[0]
        # yDistance = bottomPos[1] - topPos[1]
        # zDistance = bottomPos[2] + 1 - topPos[2]
        # boxPositionDifference = (xDistance**2 + yDistance**2 + zDistance**2)**0.5

        f = open("tmp" + str(self.solutionID) + ".txt", "w")
        f.write("%s\n%s" % (str(self.robotPositionDifference)), str(self.boxPositionDifference))
        # f.write(str(self.boxPositionDifference))
        f.close()

        os.system("mv tmp" + str(self.solutionID) + ".txt fitness" + str(self.solutionID) + ".txt")

    def Get_Positions(self, world):
        bottomPos = world.Get_Link_Positions(0)
        topPos = world.Get_Link_Positions(1)
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robot)
        basePosition = basePositionAndOrientation[0]

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