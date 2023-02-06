import pybullet as p

class WORLD:

    def __init__(self):
        self.planeId = p.loadURDF("plane.urdf")
        self.objects = p.loadSDF("world.sdf")

    def Get_Link_Positions(self, index):
        print("In get link positions")
        return p.getBasePositionAndOrientation(self.objects[index])