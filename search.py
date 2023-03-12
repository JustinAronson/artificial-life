import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import pdb
import csv
import random
import constants as c
import copy
# pdb.set_trace()
trials = []

for runNumber in range(10, c.numTrials+10):
    random.seed(runNumber)
    phc = PARALLEL_HILL_CLIMBER()
    # phc.parents[0].Start_Simulation("GUI")

    folderPath = '/Users/justin/Documents/CS Classes/artificial-life/run' + str(runNumber) + '/'
    os.makedirs(os.path.dirname(folderPath), exist_ok=True)

    phc.Evolve(folderPath)
    # phc.Show_Best('gen' + str(runNumber))
    
    # opening the csv file in 'w+' mode
    file = open(folderPath + 'fitnessData.csv', 'w+', newline ='')
    
    # writing the data into the file
    with file:   
        write = csv.writer(file)
        # print(phc.bestFitnessValues)
        write.writerows([phc.bestFitnessValues])

    finalPHC = copy.deepcopy(phc)
    trials.append(finalPHC)

input('Press Enter to continue:')

for phc in trials:
    phc.Show_Best()