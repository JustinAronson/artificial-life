import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import pdb
import csv
import random
# pdb.set_trace()
for runNumber in range(0, 5):
    random.seed(runNumber)
    phc = PARALLEL_HILL_CLIMBER()
    # phc.parents[0].Start_Simulation("GUI")

    phc.Evolve()
    phc.Show_Best('gen' + str(runNumber))
    
    # opening the csv file in 'w+' mode
    file = open('gen' + str(runNumber) + '.csv', 'w+', newline ='')
    
    # writing the data into the file
    with file:   
        write = csv.writer(file)
        # print(phc.bestFitnessValues)
        write.writerows([phc.bestFitnessValues])
