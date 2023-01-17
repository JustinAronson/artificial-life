from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time
import constants as c

class SIMULATION:

    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        p.setGravity(0, 0, -29.8)

        self.world = WORLD()
        self.robot = ROBOT()

        #pyrosim.Prepare_To_Simulate(self.robot.robotId)

    def __del__(self):
        p.disconnect()


    def Run(self):
        for t in range(0, c.loopIterations):
            time.sleep(1/240)
            p.stepSimulation()

            self.robot.Sense(t)

            # pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = b'Torso_BackLeg',
            #     controlMode = p.POSITION_CONTROL, targetPosition = targetAnglesBack[i], maxForce = 200)
            # pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = b'Torso_FrontLeg',
            #     controlMode = p.POSITION_CONTROL, targetPosition = targetAnglesFront[i], maxForce = 200)