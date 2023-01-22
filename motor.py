import constants as c
import numpy
import pyrosim.pyrosim as pyrosim
import pybullet as p

class MOTOR:

    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.amplitudeBack
        self.frequency = c.frequencyBack
        self.offset = c.phaseOffsetBack

        self.targetAngles = numpy.linspace(0, 2 * numpy.pi, c.loopIterations)
        self.motorValues = self.amplitude * numpy.sin(self.targetAngles * self.frequency + self.offset)


    def Set_Value(self, robot, t):
        pyrosim.Set_Motor_For_Joint(bodyIndex = robot, jointName = self.jointName,
                controlMode = p.POSITION_CONTROL, targetPosition = self.motorValues[t], maxForce = 200)