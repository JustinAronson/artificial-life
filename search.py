import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER

phc = PARALLEL_HILL_CLIMBER()
# phc.Evaluate(self.parents)
phc.parents[0].Start_Simulation("GUI")
# for id in phc.parents:
#     solutions[id].Start_Simulation("DIRECT")
# for id in solutions:
#     solutions[id].Wait_For_Simulation_To_End()

# Uncomment Later
# phc.Evolve()
# phc.Show_Best()


# for i in range (0, 5):
#     os.system("python3 generate.py")
#     os.system("python3 simulate.py")
