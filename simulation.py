from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time
import constants as c

class SIMULATION:

    def __init__(self, directOrGUI, solutionID):
        self.directOrGUI = directOrGUI
        if self.directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        p.setGravity(0, 0, -9.8)

        self.world = WORLD()
        self.robot = ROBOT(solutionID)

        #pyrosim.Prepare_To_Simulate(self.robot.robotId)

    def __del__(self):
        p.disconnect()


    def Run(self):
        for t in range(0, c.loopIterations):
            if self.directOrGUI == "GUI":
                time.sleep(1/2400)
            p.stepSimulation()

            self.robot.Sense(t)
            self.robot.Think()
            self.robot.Act(t)
            self.robot.Get_Positions(self.world)

    def Get_Fitness(self):
        self.robot.Get_Fitness()