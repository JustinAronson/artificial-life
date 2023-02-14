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
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
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

            bottomBoxPos = self.world.Get_Link_Positions(0)
            topBoxPos = self.world.Get_Link_Positions(0)

            self.robot.Find_Fitness(bottomBoxPos, topBoxPos)

    def Get_Fitness(self):
        self.robot.Get_Fitness()