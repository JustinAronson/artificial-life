import pybullet as p
import time
import pybullet_data
import generate
import pyrosim.pyrosim as pyrosim
import numpy

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")


p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)

loopIterations = 200
backLegSensorValues = numpy.zeros(loopIterations)
frontLegSensorValues = numpy.zeros(loopIterations)

for i in range(0, loopIterations):
    time.sleep(1/20)
    p.stepSimulation()

    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

p.disconnect()

numpy.save('data//backLegVals', backLegSensorValues)
numpy.save('data//frontLegVals', frontLegSensorValues)