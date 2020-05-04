# Amanda Lawrence
# Team Pandemic
# CS 467 - Online Capstone
# Created: 04/30/2020
# Modified: 05/01/2020
# model.py

# This program represents a SEIR model which represents infections as they spread through a population.
# For reference, see: https://www.idmod.org/docs/hiv/model-seir.html#seir-model
# In a SEIR model, individuals move through each compartment (Susceptible, Exposed, Infectious, Recovered). 
# This model assumes that after a person has recovered, they cannot be reinfected.
# This model is also not taking into account births or deaths into its calculations.
# Where N = S+E+I+R is the total population.
#
# We will use the following variables in calculations:
#	beta = infectious rate; calculating the probability of transmitting disease between an Infected to a Susceptible individual, leaving them Exposed.
#	sigma = incubation rate; the rate of latent individuals becoming infectious (average rate of duration is 1/S)
#	gamma = recovery rate; 1/D; is determined by the average duration, D.
#	xi = the rate which recovered individuals return to the susceptible state due to loss of immunity.


from pandas import DataFrame, read_csv
from time import sleep
from datetime import datetime
import pandas as pd
import numpy as np
import glob
import os
import shutil
import json

import matplotlib.pyplot as plt






# def calculate_delta_susceptible():
# 	#function here
# 	print("SUSCEPTIBLE FUNCTION")


# def calculate_delta_exposed():
# 	#function here
# 	print("EXPOSED FUNCTION")


# def calculate_delta_infected():
# 	#function here
# 	print("INFECTED FUNCTION")


# def calculate_delta_recovered():
# 	#function here
# 	print("RECOVERED FUNCTION")







def infect(Istart=0.01, Sstart=0.99, Rstart=0, transm=3.2, recov=0.23, maxT=1, nsteps=10):
	#tvals = np.linspace(0, maxT, nsteps)
	tstep = float(maxT) / float(nsteps)
	Rcurr = Rstart
	Scurr = Sstart
	Icurr = Istart
	tvals = [0.0]
	Rvals = [Rstart]
	Svals = [Sstart]
	Ivals = [Istart]
	#tsirs = [(0.0, Sstart, Istart, Rstart)]
	#for t in tvals:
	tcurr = 0.0
	for step in range(nsteps):
		deltaS = -transm * Scurr * Icurr * tstep
		deltaR = recov * Icurr * tstep
		deltaI = tstep * (transm * Scurr * Icurr - recov * Icurr)
		Scurr += deltaS
		Icurr += deltaI
		Rcurr += deltaR
		tcurr += tstep
		total = Scurr + Icurr + Rcurr
		Svals.append(Scurr)
		Ivals.append(Icurr)
		Rvals.append(Rcurr)
		tvals.append(tcurr)
		#tsirs.append((tcurr, Scurr, Icurr, Rcurr))

		print("At time %.3f, have S=%.3f, I=%.3f, R=%.3f | total=%.3f" % (tcurr, Scurr, Icurr, Rcurr, total))
	return tvals, Svals, Ivals, Rvals
	#return np.array(tsirs)
	#return tvals, np.array(Svals), np.array(Ivals), np.array(Rvals)







if __name__ == '__main__':
	print("RUN MODEL")
	

	TT, SS, II, RR = infect(maxT=15, nsteps=1000)


	plt.clf()
	plt.grid(True)
	plt.plot(TT, SS, label='SS')
	plt.plot(TT, II, label='II')
	plt.plot(TT, RR, label='RR')
	plt.legend(loc='upper right')
	plt.show()  # interactive
	#plt.savefig('SIR.png')





	