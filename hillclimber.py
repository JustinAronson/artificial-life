import pybullet as p
from solution import SOLUTION
import constants as c
import copy

class HILL_CLIMBER:

    def __init__(self):
        self.parent = SOLUTION()
        print("Out HILL_CLIMBER")

    def Evolve(self):
        self.parent.Evaluate("GUI")
        for currentGeneration in range(0, c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")
        self.Print()
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.child.Mutate()

    def Select(self):
        if self.child.fitness < self.parent.fitness:
            self.parent = self.child

    def Print(self):
        print('Parent fitness: ' + str(self.parent.fitness))
        print('Child fitness: ' + str(self.child.fitness))

    def Show_Best(self):
        self.parent.Evaluate("GUI")