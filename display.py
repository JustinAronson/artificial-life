import pickle
from solution import SOLUTION
import constants as c

for runNumber in range(0, c.numTrials):
    robot = SOLUTION(runNumber)

    favorite_color = pickle.load( open( "save.p", "rb" ) )  
    robot.linkPlan = pickle.load( open( 'gen' + str(runNumber) + "linkPlan.p", "rb" ) )
    robot.jointPlan = pickle.load( open( 'gen' + str(runNumber) + "jointPlan.p", "rb" ) )
    robot.sensorWeights = pickle.load( open( 'gen' + str(runNumber) + "sensorWeights.p", "rb" ) )
    robot.motorWeights = pickle.load( open( 'gen' + str(runNumber) + "motorWeights.p", "rb" ) )

    robot.Start_Simulation("GUI")