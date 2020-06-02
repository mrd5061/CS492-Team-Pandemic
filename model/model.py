# Amanda Lawrence
# Team Pandemic
# CS 467 - Online Capstone
# Created: 04/30/2020
# Modified: 05/25/2020
# model.py

# To use virtual environment, In Terminal use: source ~/venv/pandemic_model/bin/activate

# This program represents a SIR model which represents infections as they spread through a population.
# For reference, see: https://www.idmod.org/docs/hiv/model-sir.html
# In a SIR model, individuals move through each compartment (Susceptible, Infectious, Recovered). 
# This model assumes that after a person has recovered, they cannot be reinfected.
# This model is also not taking into account births or deaths into its calculations.
# Where N = S+I+R is the total population.


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





def argnear(vec, val):
    return (np.abs(vec - val)).argmin()




##--------------------------------------------------------------------------##
##	Infect will compute the SIR model, and does not yet take into account 
##	any given timescale. The fitting.py script will take into account days
##--------------------------------------------------------------------------## 

def infect(Istart=0.000001, Rstart=0, transm=3.2, recov=0.23, maxT=1, nsteps=10):
	Sstart = 1. - Rstart - Istart
	tstep = 1.0 / float(nsteps)
	niters = int(maxT*nsteps)
	Rcurr = Rstart
	Scurr = Sstart
	Icurr = Istart
	tvals = [0.0]
	Rvals = [Rstart]
	Svals = [Sstart]
	Ivals = [Istart]
	tcurr = 0.0
	for step in range(niters):
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

	return np.array(tvals), np.array(Svals), np.array(Ivals), np.array(Rvals)






if __name__ == '__main__':
	print("RUN MODEL")
	

	TT, SS, II, RR = infect(maxT=15, nsteps=1000)


	plt.clf()
	plt.grid(True)
	plt.plot(TT, SS, label='SS')
	plt.plot(TT, II, label='II')
	plt.plot(TT, RR, label='RR')
	plt.plot(TT, 1-np.array(SS), label='CC') #cumulative confirmed cases
	plt.legend(loc='upper right')
	plt.show()  # interactive
	#plt.savefig('SIR.png')





	