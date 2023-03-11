import pickle
import constants as c
import pybullet as p
import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import math

os.system("rm brain*.nndf")
os.system("rm body*.urdf")

#Enter the run number and generation you want to see:
runNumber = 0
generation = 0

def Create_Body(linkPlan, jointPlan, sensorWeights, motorWeights):
    pyrosim.Start_URDF("body0.urdf")
            
    Create_Links()

    pyrosim.End()

def Create_Links():
    for link in linkPlan:
        pyrosim.Send_Cube(name=str(link[0]), pos=link[2], size=link[3], colorName = link[4])
    for joint in jointPlan:
        pyrosim.Send_Joint(name = str(joint[0]) + "_" + str(joint[1]) , parent= str(joint[0]) , child = str(joint[1]) , type = "revolute", position = joint[2], jointAxis = "1 1 0")

def Create_Brain(linkPlan, jointPlan, sensorWeights, motorWeights):
    pyrosim.Start_NeuralNetwork("brain0.nndf")

    sensorIndex = 0
    sensors = []
    for link in linkPlan:
        if link[4] == 'green':
            pyrosim.Send_Sensor_Neuron(name = sensorIndex + len(jointPlan) + numHiddenNeurons , linkName = str(link[0]))
            # self.sensors.append(link[0])       
            # sensorIndex += 1
            if link[0] not in sensorWeights:
                sensorWeights[link[0]] = []
                for i in range(0, numHiddenNeurons):
                    sensorWeights[link[0]].append(random.random() * 2 - 1)

            for i in range(0, numHiddenNeurons):
                hiddenNeuronName = len(jointPlan) + i
                pyrosim.Send_Synapse( sourceNeuronName = sensorIndex + len(jointPlan) + numHiddenNeurons , targetNeuronName = hiddenNeuronName , weight = sensorWeights[link[0]][i] )

            sensors.append(link[0])     
            sensorIndex += 1
        
    # print("Sensors: ")
    # print(self.sensors)

    for joint in jointPlan:
        pyrosim.Send_Motor_Neuron( name = jointPlan.index(joint) , jointName = str(joint[0]) + "_" + str(joint[1]))

        if jointPlan.index(joint) not in motorWeights:
            motorWeights[jointPlan.index(joint)] = []
            for i in range(0, numHiddenNeurons):
                motorWeights[jointPlan.index(joint)].append(random.random() * 2 - 1)

        for i in range(0, numHiddenNeurons):
            hiddenNeuronName = len(jointPlan) + i
            pyrosim.Send_Synapse( sourceNeuronName = hiddenNeuronName , targetNeuronName = jointPlan.index(joint) , weight = motorWeights[jointPlan.index(joint)][i] )

    for hiddenNeuronID in range(0, numHiddenNeurons):
        pyrosim.Send_Hidden_Neuron(name = len(jointPlan) + hiddenNeuronID)

    pyrosim.End()

folderPath = '/Users/justin/Documents/CS Classes/artificial-life/run' + str(runNumber) + '/'

linkPlan = pickle.load( open( folderPath + "Gen" + str(generation) + "linkPlan.p", "rb" ) )
jointPlan = pickle.load( open( folderPath + "Gen" + str(generation) + "jointPlan.p", "rb" ) )
sensorWeights = pickle.load( open( folderPath + "Gen" + str(generation) + "sensorWeights.p", "rb" ) )
motorWeights = pickle.load( open( folderPath + "Gen" + str(generation) + "motorWeights.p", "rb" ) )
# numHiddenNeurons = pickle.load( open( folderPath + "Gen" + str(generation) + "hiddenNeurons.p", "wb" ) )

numHiddenNeurons = len(sensorWeights[0])

Create_Body(linkPlan, jointPlan, sensorWeights, motorWeights)
Create_Brain(linkPlan, jointPlan, sensorWeights, motorWeights)

os.system("python3 simulate.py " + "GUI" + " " + str(0) + " 2&>1 &")