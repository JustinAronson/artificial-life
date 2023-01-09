import pybullet as p
import time

physicsClient = p.connect(p.GUI)

p.loadSDF("box.sdf")

for i in range(0, 1000):
    time.sleep(1/60)
    p.stepSimulation()

    print(i)

p.disconnect()