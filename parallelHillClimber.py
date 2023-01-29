import pybullet as p
from solution import SOLUTION
import constants as c
import copy

class PARALLEL_HILL_CLIMBER:

    def __init__(self):
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(0, c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        # self.parent = SOLUTION()
        # print("Out HILL_CLIMBER")

    def Evolve(self):
        for parent in self.parents:
            self.parents[parent].Evaluate("GUI")
        # self.parent.Evaluate("GUI")
        # for currentGeneration in range(0, c.numberOfGenerations):
        #     self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")
        self.Print()
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)
        self.child.Set_ID(self.nextAvailableID)
        self.nextAvailableID += 1

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