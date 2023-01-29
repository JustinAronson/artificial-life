import pybullet as p
import time
import pybullet_data
#import generate
import pyrosim.pyrosim as pyrosim
import numpy
import random
import math
import matplotlib.pyplot as matplotlib
import constants as c
from simulation import SIMULATION
import sys

directOrGUI = sys.argv[1]

simulation = SIMULATION(directOrGUI)

simulation.Run()
simulation.Get_Fitness()