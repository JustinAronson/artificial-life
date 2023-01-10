import pybullet as p
import time
import pybullet_data
import generate

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")


p.loadSDF("world.sdf")

for i in range(0, 1000):
    time.sleep(1/20)
    p.stepSimulation()

    print(i)

p.disconnect()