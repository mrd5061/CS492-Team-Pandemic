#!/usr/bin/env python
# vim: set fileencoding=utf-8 ts=4 sts=4 sw=4 et tw=80 :
# To use virtual environment, In Terminal use: source ~/venv/pandemic_model/bin/activate
#
# Amanda Lawrence
# Created: 05/08/2020
# Modified: 05/25/2020
#
# Imports and fits data to our model
#   

# Python version-agnostic module reloading:
try:
    reload                              # Python 2.7
except NameError:
    try:
        from importlib import reload    # Python 3.4+
    except ImportError:
        from imp import reload          # Python 3.0 - 3.3


import glob
import gc
import os
import sys
import time
import numpy as np
import datetime as dt
import scipy.optimize as opti
from functools import partial
import matplotlib.pyplot as plt
import pandas as pd
import sqlalchemy
from sqlalchemy import Column, create_engine, select, MetaData,Table,text
import model
reload(model)


try:
	import astropy.time as astt
except ImportError:
    sys.stderr.write("\nError: astropy module not found!\n")
    sys.exit(1)





def argnear(vec, val):
    print("RECEIVED VEC OF:  ")
    print(vec)
    absolute_value = []
    for vec_value in vec:
        absolute_value = absolute_value.append(np.abs(vec_value - val))
    return (absolute_value).argmin()


##--------------------------------------------------------------------------##
##
##  infectify() will compute our model and return the outputs:
##      fTT = time in days, from 01/22/2020
##      SS = fraction of population that is susceptible
##      II = fraction of population that is infected
##      RR = fraction of population that has recovered
##      On any given day, SS+II+RR should equal 1, and each of the values of
##      SS, II, RR must each be >= 0 and <= 1. 
##
##--------------------------------------------------------------------------##
def infectify(params, maxT=3, nsteps=10000, Tscale=9.):
    T_start, transm = params
    TT, SS, II, RR = model.infect(maxT=maxT, transm=transm, nsteps=nsteps) #, Istart=Istart) #, transm=5)
    fTT = Tscale*TT + T_start # T_start=number of days since 01/22/2020
    return fTT, SS, II, RR



##--------------------------------------------------------------------------##
#   The merit function. This function returns the sum of the squares of the 
##  residuals. Describes the goodness or badness of what we're evaluating.
##--------------------------------------------------------------------------##
def trial_infection(params, times_data, cases_data):
    fTT, SS, II, RR = infectify(params)
    all_confirmed = population * (1.0-SS)
    cyvals = np.interp(times_data, fTT, all_confirmed)
    residuals = cases_data - cyvals
    return np.sum(residuals**2)


##--------------------------------------------------------------------------##
##  Cleans up the date format
##--------------------------------------------------------------------------##
def timefix(when):
    yy, mm, dd = (x for x in str(when).split('-'))
    return dt.datetime(int(yy), int(mm), int(dd))



##--------------------------------------------------------------------------##
##  Runs the model, on our selected transmission rate and outputs 
##  projected time values, projected susceptible population amount, 
##  projected infected population amount, and projected recovered population amount
##--------------------------------------------------------------------------##
def make_projections(I_start, R_start, projected_transm):
    return model.infect(I_start, R_start, projected_transm, nsteps=1000)


##--------------------------------------------------------------------------##
##  The setup for a database connection to our PostgreSQL database, from pulling 
##  data from PostgreSQL in lieu of the John Hopkins csv files.
##--------------------------------------------------------------------------##

engine = sqlalchemy.create_engine("postgres://postgres:pandemic1234@pandemicdb.cehiwrdshmps.us-east-1.rds.amazonaws.com/pandemicdb")

db_conn = engine.connect()

#dict of states to iterate through. the key represents the STATE_OR_PROVINCE.STATE_ID for each state 
state ={60:'Alabama', 61: 'Alaska', 62: 'Arizona', 63: 'Arkansas', 64: 'California', 65: 'Colorado', 66: 'Connecticut', 67: 'District of Columbia', 68: 'Delaware', 69: 'Florida', 70: 'Georgia', 71: 'Hawaii', 72: 'Idaho', 73: 'Illinois', 74: 'Indiana', 75: 'Iowa', 76: 'Kansas', 77: 'Kentucky', 78: 'Louisiana', 79: 'Maine', 80: 'Maryland', 81: 'Massachusetts' , 82: 'Michigan', 83: 'Minnesota', 84: 'Mississippi', 85: 'Missouri', 86: 'Montana', 87: 'Nebraska', 88: 'Nevada', 89: 'New Hampshire', 90: 'New Jersey', 91: 'New Mexico', 92: 'New York', 93: 'North Carolina', 94: 'North Dakota', 95: 'Ohio', 96: 'Oklahoma', 97: 'Oregon', 98: 'Pennsylvania', 99: 'Rhode Island', 100: 'South Carolina', 101: 'South Dakota', 102: 'Tennessee', 103: 'Texas', 104: 'Utah', 105: 'Vermont', 106: 'Virginia', 107: 'Washington', 108: 'West Virginia', 109: 'Wisconsin', 110: 'Wyoming', 111: 'American Samoa', 112: 'Guam', 113: 'North Mariana Islands', 114: 'Puerto Rico', 115: 'Virgin Islands'}

##--------------------------------------------------------------------------##
##  SQL queries to pull data for the number of confirmed cases, and each state population
##--------------------------------------------------------------------------##

result = db_conn.execute("""SELECT * FROM test."REPORTED_CASES"
ORDER BY "CASES_ID" ASC """).fetchall()

pop_result = db_conn.execute("""SELECT * FROM test."STATE_OR_PROVINCE"
    ORDER BY "STATE_ID" ASC """).fetchall()

print("RESULT LOOKS LIKE:  ")
print(result)

##--------------------------------------------------------------------------##
##  We look at one state at a time, and all of its dates and the corresponding 
##  active cases, and place it into a dictionary
##--------------------------------------------------------------------------##
# creates a dictionary object of state ID number and population amount. 
state_population_dict = {x[0]:x[6] for x in pop_result}


# For each ID that appears in state_population_dict[0], we will gather any rows from the REPORTED_CASES 
# table in order to run or model and create projections on that. 
#for each_state in state_population_dict:
for each_state_id in range(60, 111):

    print("RUNNING FOR STATE ID:  ")
    print(each_state_id)
    # Creates a list of lists, containing the confirmed cases, for all dates retrieved from 
    # the REPORTED_CASES table, for a single state.
    confirmed_cases_objects = list(filter(lambda x: x[1]==each_state_id, result))

    #Sorts this list of lists, based on the date
    confirmed_cases_objects.sort(key=lambda x: x[3])

    print("CONFIRMED CASES OBJECTS IS:  ")
    print(confirmed_cases_objects)

    timestamp = astt.Time([timefix(x[3]) for x in confirmed_cases_objects], scale='utc')
    days_elapsed = timestamp.jd - timestamp.jd.min()
    print("DAYS_ELAPSED ARE:  ")
    print(days_elapsed)

    _, _, cases, dates = zip(*confirmed_cases_objects)
    total_per_date = np.array(cases)
    population = state_population_dict[each_state_id]


    ##--------------------------------------------------------------------------##
    ##  Fits a line to the last 14 days, in order to extrapolate 
    ##  and draw a line of the next several days of confirmed cases
    ##--------------------------------------------------------------------------##

    lookback_days = 14. # The number of days back, from the end of the dataset, to use in evaluating our projection 
    which = (days_elapsed>days_elapsed.max()-lookback_days) #returns boolean array for which dates meet this criteria

    ##--------------------------------------------------------------------------##
    ##  Additional projections, dependent on a change in the transmission rate 
    ##  indicating that stay-at-home measures may either become stricter or more lenient.
    ##  The user will be able to choose from multiple options, on what a projection
    ##  would look like, for any given state, and the transmission rate will either 
    ##  increase or decrease.  
    ##
    ##  By default, the model is using transm = 3.2. 4, 3.5, 3.2, 3, 2.5
    ##--------------------------------------------------------------------------##

    projection_RR = total_per_date[-14]
    projection_II = total_per_date[-1]-projection_RR
    I_start = projection_II/population
    R_start = projection_RR/population




    projected_TT, projected_SS, projected_II, projected_RR = make_projections(I_start, R_start, 0.5) #returns arrays of time, Susceptible, Infected, and Recovered 
    projected_TT = 9.*projected_TT + days_elapsed.max()
    projected_CC = 1.0 - projected_SS
    projected_CC *= population #projected confirmed cases

    ##--------------------------------------------------------------------------##
    ## Plotting out the results of our fitting
    ##--------------------------------------------------------------------------##

    for r in [4, 3, 2, 1, 0.5]:
        projected_TT, projected_SS, projected_II, projected_RR = make_projections(I_start, R_start, r) #returns arrays of time, Susceptible, Infected, and Recovered 
        #projected_TT = 9.*projected_TT + days_elapsed.max()
        projected_TT = 9.*projected_TT + days_elapsed.max()
        projected_CC = 1.0 - projected_SS
        projected_CC *= population #projected confirmed cases
        future_TT = projected_TT - projected_TT.min()
        days_of_projection = np.array([1, 2, 3, 4, 5, 6, 7])
        cumulative_cases_of_projection = np.interp(days_of_projection, future_TT, projected_CC)
        ##--------------------------------------------------------------------------##
        ##  Insert data into PostgreSQL database, to the FITTED_DATA table, one projection
        ##  at a time.
        ##--------------------------------------------------------------------------##
        insert_statement = """INSERT INTO "FITTED_DATA"    
        ("STATE_ID","DATE_REPORTED","TRANS_RATE", "DAY_1", "DAY_2", "DAY_3", "DAY_4", "DAY_5", "DAY_6", "DAY_7")
        VALUES ( {}, '{}', {}, {}, {}, {}, {}, {}, {}, {})""".format(
        each_state_id, dates[-1], r, *cumulative_cases_of_projection)
        db_conn.execute(insert_statement)




##--------------------------------------------------------------------------##
##  Close PostgreSQL database connection
##--------------------------------------------------------------------------##
db_conn.close()



