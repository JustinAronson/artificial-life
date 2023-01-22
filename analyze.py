import numpy
import matplotlib.pyplot as matplotlib

backLegSensorValues  = numpy.load('data//backLegVals.npy')
frontLegSensorValues  = numpy.load('data//frontLegVals.npy')

matplotlib.plot(backLegSensorValues, label='backLeg', linewidth='2.5')
matplotlib.plot(frontLegSensorValues, label='frontLeg')

matplotlib.legend()
matplotlib.show()
