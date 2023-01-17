import pybullet as p
import time
import pybullet_data
import generate
import pyrosim.pyrosim as pyrosim
import numpy
import random
import math
import matplotlib.pyplot as matplotlib

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -29.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")


p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)

amplitudeBack = numpy.pi/4
frequencyBack = 3
phaseOffsetBack = 0
amplitudeFront = numpy.pi/4
frequencyFront = 6
phaseOffsetFront = numpy.pi/4

loopIterations = 1000
backLegSensorValues = numpy.zeros(loopIterations)
frontLegSensorValues = numpy.zeros(loopIterations)

targetAngles = numpy.linspace(0, 2 * numpy.pi, loopIterations)
targetAnglesBack = amplitudeBack * numpy.sin(targetAngles * frequencyBack + phaseOffsetBack)
targetAnglesFront = amplitudeFront * numpy.sin(targetAngles * frequencyFront + phaseOffsetFront)

# matplotlib.plot(targetAngles)
# matplotlib.show()
# exit()

for i in range(0, loopIterations):
    time.sleep(1/240)
    p.stepSimulation()

    # backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    # frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")



    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = b'Torso_BackLeg',
        controlMode = p.POSITION_CONTROL, targetPosition = targetAnglesBack[i], maxForce = 200)
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = b'Torso_FrontLeg',
        controlMode = p.POSITION_CONTROL, targetPosition = targetAnglesFront[i], maxForce = 200)


p.disconnect()

numpy.save('data//backLegVals', backLegSensorValues)
numpy.save('data//frontLegVals', frontLegSensorValues)