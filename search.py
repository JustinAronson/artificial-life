import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import pdb;
# pdb.set_trace()

phc = PARALLEL_HILL_CLIMBER()
# phc.parents[0].Start_Simulation("GUI")

# Uncomment Later
phc.Evolve()
phc.Show_Best()


# for i in range (0, 5):
#     os.system("python3 generate.py")
#     os.system("python3 simulate.py")
