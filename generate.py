import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")

length = 1
width = 1
height = 1

x = 0
y = 0

for row in range(0, 3):
    y = 0

    for column in range(0, 3):
        length = 1
        width = 1
        height = 1
        z = height/2
        
        for i in range (0, 10):
            pyrosim.Send_Cube(name="Box" + str(i) + str(row) + str(column), pos=[x, y, z], size=[length, width, height])

            z += height

            length *= 0.9
            width *= 0.9
            height *= 0.9

        y += 1
    x += 1

#pyrosim.Send_Cube(name="Box2", pos=[x, y, z], size=[length, width, height])


pyrosim.End()