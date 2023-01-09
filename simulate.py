import pybullet as p
import time

physicsClient = p.connect(p.GUI)

for i in range(0, 1000):
    time.sleep(1/2000)
    p.stepSimulation()

    print(i)

p.disconnect()