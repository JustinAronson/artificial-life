import pybullet as p
from solution import SOLUTION
import constants as c
import copy
import os
import pickle

class PARALLEL_HILL_CLIMBER:

    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        os.system("rm body*.urdf")

        self.parents = {}
        self.nextAvailableID = 0
        for i in range(0, c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        # self.parent = SOLUTION()
        # print("Out HILL_CLIMBER")
        self.bestFitnessValues = []

    def Evolve(self):
        self.Evaluate(self.parents)
        # self.parent.Evaluate("GUI")
        for currentGeneration in range(0, c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        # self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}
        for id in self.parents:
            self.children[id] = copy.deepcopy(self.parents[id])
            self.children[id].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for id in self.children:
            self.children[id].Mutate()

    def Select(self):
        minFitness = 10000
        for id in self.parents:
            if self.children[id].fitness < self.parents[id].fitness:
                self.parents[id] = self.children[id]

            if self.parents[id].fitness < minFitness:
                minFitness = self.parents[id].fitness

        self.bestFitnessValues.append(minFitness)

    def Print(self):
        for id in self.parents:
            print("")
            print('Parent fitness: ' + str(self.parents[id].fitness))
            print('Child fitness: ' + str(self.children[id].fitness))
            print("")

    def Show_Best(self, fileName):
        lowestFitnessParent = self.parents[0]
        for id in self.parents:
            if self.parents[id].fitness < lowestFitnessParent.fitness:
                lowestFitnessParent = self.parents[id]
        
        pickle.dump( lowestFitnessParent.linkPlan, open( fileName + "linkPlan.p", "wb" ) )
        pickle.dump( lowestFitnessParent.jointPlan, open( fileName + "jointPlan.p", "wb" ) )
        pickle.dump( lowestFitnessParent.sensorWeights, open( fileName + "sensorWeights.p", "wb" ) )
        pickle.dump( lowestFitnessParent.motorWeights, open( fileName + "motorWeights.p", "wb" ) )
        
        lowestFitnessParent.Start_Simulation("GUI")

    def Evaluate(self, solutions):
        for id in solutions:
            solutions[id].Start_Simulation("DIRECT")
        for id in solutions:
            solutions[id].Wait_For_Simulation_To_End()