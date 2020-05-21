#!/usr/bin/env python
# vim: set fileencoding=utf-8 ts=4 sts=4 sw=4 et tw=80 :
# To use virtual environment, In Terminal use: source ~/venv/pandemic_model/bin/activate
#
# Amanda Lawrence
# Created: 05/08/2020
# Modified: 05/08/2020
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
#import statsmodels.api as sm
#import statsmodels.formula.api as smf



try:
	import astropy.time as astt
except ImportError:
    #logger.error("astropy module not found!  Install and retry.")
    sys.stderr.write("\nError: astropy module not found!\n")
    sys.exit(1)

def argnear(vec, val):
    return (np.abs(vec - val)).argmin()




##--------------------------------------------------------------------------##
##  The setup for pulling data directly from the raw data csv files from 
##  John Hopkins.
##--------------------------------------------------------------------------##
# Load data:
base_csv_dir = '../datasets/'
cumu_csv_dir = os.path.join(base_csv_dir, 'csse_covid_19_daily_reports')
time_csv_dir = os.path.join(base_csv_dir, 'csse_covid_19_time_series')
#prefix = 'time_series_19-covid'
#csv_files = sorted(glob.glob('%s/*.csv' % time_csv_dir))

data = {}
#csv_names = ['Confirmed', 'Deaths', 'Recovered']
csv_names = ['confirmed', 'deaths', 'recovered']
data['confirmed'] = pd.read_csv("../datasets/time_series_covid19_confirmed_US_04_20_2020.csv")
data['deaths'] = pd.read_csv("../datasets/time_series_covid19_deaths_US_04_20_2020.csv")
case = data['confirmed']
number_cols = slice(11, None, None)
date_strings = case.keys()[number_cols]

##--------------------------------------------------------------------------##
##  The setup for a database connection to our PostgreSQL database, from pulling 
##  data from PostgreSQL in lieu of the John Hopkins csv files.
##--------------------------------------------------------------------------##

engine = sqlalchemy.create_engine("postgres://postgres:pandemic1234@pandemicdb.cehiwrdshmps.us-east-1.rds.amazonaws.com/pandemicdb")

db_conn = engine.connect()

#dict of states to iterate through. the key represents the STATE_OR_PROVINCE.STATE_ID for each state 
state ={60:'Alabama', 61: 'Alaska', 62: 'Arizona', 63: 'Arkansas', 64: 'California', 65: 'Colorado', 66: 'Connecticut', 67: 'District of Columbia', 68: 'Delaware', 69: 'Florida', 70: 'Georgia', 71: 'Hawaii', 72: 'Idaho', 73: 'Illinois', 74: 'Indiana', 75: 'Iowa', 76: 'Kansas', 77: 'Kentucky', 78: 'Louisiana', 79: 'Maine', 80: 'Maryland', 81: 'Massachusetts' , 82: 'Michigan', 83: 'Minnesota', 84: 'Mississippi', 85: 'Missouri', 86: 'Montana', 87: 'Nebraska', 88: 'Nevada', 89: 'New Hampshire', 90: 'New Jersey', 91: 'New Mexico', 92: 'New York', 93: 'North Carolina', 94: 'North Dakota', 95: 'Ohio', 96: 'Oklahoma', 97: 'Oregon', 98: 'Pennsylvania', 99: 'Rhode Island', 100: 'South Carolina', 101: 'South Dakota', 102: 'Tennessee', 103: 'Texas', 104: 'Utah', 105: 'Vermont', 106: 'Virginia', 107: 'Washington', 108: 'West Virginia', 109: 'Wisconsin', 110: 'Wyoming', 111: 'American Samoa', 112: 'Guam', 113: 'North Mariana Islands', 114: 'Puerto Rico', 115: 'Virgin Isalnds'}


#for k, v in state.items():
#db_conn.execute("""INSERT INTO "REPORTED_CASES" 
#    ("STATE_ID","NUM_CASES","DATE_REPORTED")
#    VALUES ( {},(SELECT SUM("{}") FROM import.times_report_confirmed WHERE "Province_State" = '{}'),'{}')""".format(k,dString,v,dString,v))

result = db_conn.execute("""SELECT * FROM test."REPORTED_ACTIVE"
ORDER BY "ACTIVE_ID" ASC """).fetchall()

active_id, state_id, num_active, date_reported = result



def timefix(when):
    yy, mm, dd = (int(x) for x in when.split('-'))
    return dt.datetime(yy, mm, dd)

timestamp = astt.Time([timefix(x) for x in date_strings], scale='utc')
days_elapsed = timestamp.jd - timestamp.jd.min()

state_col = "Province_State"
#which_state = 'Utah'
#which_state = 'Hawaii'
#which_state = 'Massachusetts'
#which_state = 'California'
#which_state = 'Oregon'
#which_state = 'Ohio'
#which_state = 'Tennessee'
#which_state = 'Colorado'
#which_state = 'Wyoming'
#which_state = 'Louisiana'
which_state = 'Florida'

#county_data = case[case[state_col] == which_state]

total_per_date = county_data[date_strings].sum(axis=0)

T_start = days_elapsed[argnear(total_per_date, 3)]

#utah_pop = 3205958
#hawaii_pop = 1415872
#massachusetts_pop = 6892503
#california_pop = 39512223
#oregon_pop = 4217737
#ohio_pop = 11689100
#tennessee_pop = 6829174
#colorado_pop = 5758736
#wyoming_pop = 578759
#louisiana_pop = 4648794
florida_pop = 21477737

#population = utah_pop
#population = hawaii_pop
#population = massachusetts_pop
#population = california_pop
#population = oregon_pop
#population = ohio_pop
#population = tennessee_pop
#population = colorado_pop
#population = wyoming_pop
#population = louisiana_pop
population = florida_pop

#Time scale
#T_scale = 74.


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
    #T_start, Istart, transm = params
    T_start, transm = params
    TT, SS, II, RR = model.infect(maxT=maxT, transm=transm, nsteps=nsteps) #, Istart=Istart) #, transm=5)
    fTT = Tscale*TT + T_start # T_start=number of days since 01/22/2020
    return fTT, SS, II, RR


##--------------------------------------------------------------------------##

# Select which points to fit. We will ignore days where the confirmed cases equal 0
which = (total_per_date.values > 0) & (days_elapsed>70)

# The times and case counts we are attempting to fit the model to. 
keep_times = days_elapsed[which]
keep_cases = total_per_date.values[which]

# fitted parameters:
# [T_start, transm]

##--------------------------------------------------------------------------##
#   The merit function. This function returns the sum of the squares of the 
##  residuals. Describes the goodness or badness of what we're evaluating.
##--------------------------------------------------------------------------##
def trial_infection(params, times_data, cases_data):
    fTT, SS, II, RR = infectify(params)
    all_confirmed = population * (1.0-SS)
    #fTT = TT + T_start

    cyvals = np.interp(times_data, fTT, all_confirmed)

    residuals = cases_data - cyvals
    #residuals = np.log(cases_data) - np.log(cyvals)
    return np.sum(residuals**2)

#crapper = partial(trial_infection, times_data=keep_times, cases_data=keep_cases)

# pguess is the parameter guess, makes an initial guess
pguess = np.array([40, 0.001, 3])
pguess = np.array([40, 3])
dargs = (keep_times, keep_cases)



# awesome holds the resulting of our fitting, which is computed using trial_infection(), parameter guess, times and case counts we're attempting to fit model to.
awesome = opti.fmin(trial_infection, pguess, dargs, maxiter=10)


#pTT = T_scale*TT + awesome[0]
print("best-fit parameters: %s" % str(awesome))
#nyc_days = 42.
#nyc_cinf = 0.05
#TT, SS, II, RR = model.infect(maxT=5, nsteps=100000) #, transm=5)
pTT, SS, II, RR = infectify(awesome)
all_confirmed = 1.0-SS
pSS = SS*population
pII = II*population
pRR = RR*population
all_confirmed *= population # the current state's population, times the fraction of that state's confirmed_cases

#which = argnear(1.-SS, nyc_cinf)
#sirtime = TT[argnear(1.-SS, nyc_cinf)]
#T_scale = nyc_days / sirtime
#T_scale *= 9
#T_start += 2
#pTT = T_scale*TT + T_start

#print("Using T_start=%.2f and T_scale=%.3f." % (T_start, T_scale))

##--------------------------------------------------------------------------##
##  Fits a line to the last several days, since day 70, in order to extrapolate 
##  and draw a line of the next several days of confirmed cases
##--------------------------------------------------------------------------##

lookback_days = 14. # The number of days back, from the end of the dataset, to use in evaluating our projection 
which = (days_elapsed>days_elapsed.max()-lookback_days) #returns boolean array for which dates meet this criteria

x = days_elapsed[which]

y = np.log10(total_per_date.values[which]) # for use if plotting on a logarithmic graph
#y = total_per_date.values[which]
forecast_days = 7  #The number of days beyond dataset that we would like our projection to forecast

def line(x, a, b):
    return a * x + b

popt, pcov = opti.curve_fit(line, x, y)

pY = 10**line(x, popt[0], popt[1]) # for use if plotting on a logarithmic graph
pY = line(x, popt[0], popt[1])

#ax1.plot(x, pY)
pX = np.linspace(x.min(),x.max()+forecast_days)
pY = 10**line(pX, popt[0], popt[1])

##--------------------------------------------------------------------------##
##  Additional projections, dependent on a change in the transmission rate 
##  indicating that stay-at-home measures may either become stricter or more lenient.
##  The user will be able to choose from multiple options, on what a projection
##  would look like, for any given state, and the transmission rate will either 
##  increase or decrease.  
##
##  By default, the model is using transm = 3.2. 4, 3.5, 3.2, 3, 2.5
##--------------------------------------------------------------------------##

projection_RR = total_per_date.values[-14]
projection_II = total_per_date.values[-1]-projection_RR
I_start = projection_II/population
R_start = projection_RR/population


def make_projections(I_start, R_start, projected_transm):
    return model.infect(I_start, R_start, projected_transm, nsteps=1000)


projected_TT, projected_SS, projected_II, projected_RR = make_projections(I_start, R_start, 0.5) #returns arrays of time, Susceptible, Infected, and Recovered 
projected_TT = 9.*projected_TT + days_elapsed.max()
projected_CC = 1.0 - projected_SS
projected_CC *= population #projected confirmed cases

##--------------------------------------------------------------------------##
## Plotting out the results of our fitting
##--------------------------------------------------------------------------##


#plt.style.use('bmh')   # Bayesian Methods for Hackers style
fig_dims = (7, 6)
fig = plt.figure(1, figsize=fig_dims)
#plt.gcf().clf()
fig.clf()
#fig, axs = plt.subplots(2, 2, sharex=True, figsize=fig_dims, num=1)
# sharex='col' | sharex='row'
#fig.frameon = False # disable figure frame drawing
#fig.subplots_adjust(left=0.07, right=0.95)
#ax1 = plt.subplot(gs[0, 0])
ax1 = fig.add_subplot(111)
#ax1 = fig.add_subplot(221)
#ax2 = fig.add_subplot(222)

#ax1 = fig.add_axes([0, 0, 1, 1])
#ax1.patch.set_facecolor((0.8, 0.8, 0.8))
ax1.grid(True)
#ax1.axis('off')

ax1.plot(pTT, pSS, label='SS')
ax1.plot(pTT, pII, label='II')
ax1.plot(pTT, pRR, label='RR')
ax1.plot(pTT, all_confirmed, label='CC') #cumulative confirmed cases
ax1.plot(pX, pY, c="salmon", ls="--")
#ax1.plot(projected_TT, projected_CC, label='R=4.0 projection')

for r in [4, 3, 2, 1, 0.5]:
    projected_TT, projected_SS, projected_II, projected_RR = make_projections(I_start, R_start, r) #returns arrays of time, Susceptible, Infected, and Recovered 
    projected_TT = 9.*projected_TT + days_elapsed.max()
    projected_CC = 1.0 - projected_SS
    projected_CC *= population #projected confirmed cases
    ax1.plot(projected_TT, projected_CC, label='R=%.1f projection' % r)

ax1.set_yscale('log')
ax1.set_ylim(ymin=0.5)
## Disable axis offsets:
#ax1.xaxis.get_major_formatter().set_useOffset(False)
#ax1.yaxis.get_major_formatter().set_useOffset(False)

#ax1.plot(kde_pnts, kde_vals)
#ax1.scatter(timestamp.jd, country_dead)
#ax1.scatter(fitme_jdutc, fitme_ndead)
ax1.scatter(days_elapsed, total_per_date, lw=0, s=15, label="data")
ax1.legend()
ax1.set_xlabel("days since January 22, 2020")
ax1.set_ylabel("cumulative confirmed infections")
#ax1.plot(fitted_tstamp, fitted_deaths, c='r')

#blurb = "some text"
#ax1.text(0.5, 0.5, blurb, transform=ax1.transAxes)
#ax1.text(0.5, 0.5, blurb, transform=ax1.transAxes,
#      va='top', ha='left', bbox=dict(facecolor='white', pad=10.0))
#      fontdict={'family':'monospace'}) # fixed-width

#colors = cm.rainbow(np.linspace(0, 1, len(plot_list)))
#for camid, c in zip(plot_list, colors):
#    cam_data = subsets[camid]
#    xvalue = cam_data['CCDATEMP']
#    yvalue = cam_data['PIX_MED']
#    yvalue = cam_data['IMEAN']
#    ax1.scatter(xvalue, yvalue, color=c, lw=0, label=camid)

#mtickpos = [2,5,7]
#ndecades = 1.0   # for symlog, set width of linear portion in units of dex
#nonposx='mask' | nonposx='clip' | nonposy='mask' | nonposy='clip'
#ax1.set_xscale('log', basex=10, nonposx='mask', subsx=mtickpos)
#ax1.set_xscale('log', nonposx='clip', subsx=[3])
#ax1.set_yscale('log', nonposy='clip', subsy=[3])

#ax1.set_xscale('log')
#ax1.set_yscale('log')
#ax1.set_ylim(1e-3, 1e4)

#ax1.set_yscale('symlog', basey=10, linthreshy=0.1, linscaley=ndecades)
#ax1.xaxis.set_major_formatter(formatter) # re-format x ticks
#ax1.set_ylim(ax1.get_ylim()[::-1])
#ax1.set_xlabel('whatever', labelpad=30)  # push X label down 

#ax1.set_xticks([1.0, 3.0, 10.0, 30.0, 100.0])
#ax1.set_xticks([1, 2, 3], ['Jan', 'Feb', 'Mar'])
#for label in ax1.get_xticklabels():
#    label.set_rotation(30)
#    label.set_fontsize(14) 

#ax1.xaxis.label.set_fontsize(18)
#ax1.yaxis.label.set_fontsize(18)

#ax1.set_xlim(nice_limits(xvec, pctiles=[1,99], pad=1.2))
#ax1.set_ylim(nice_limits(yvec, pctiles=[1,99], pad=1.2))

#spts = ax1.scatter(x, y, lw=0, s=5)
##cbar = fig.colorbar(spts, orientation='vertical')   # old way
#cbnorm = mplcolors.Normalize(*spts.get_clim())
#scm = plt.cm.ScalarMappable(norm=cbnorm, cmap=spts.cmap)
#scm.set_array([])
#cbar = fig.colorbar(scm, orientation='vertical')
#cbar = fig.colorbar(scm, ticks=cs.levels, orientation='vertical') # contours
#cbar.formatter.set_useOffset(False)
#cbar.update_ticks()

fig.tight_layout() # adjust boundaries sensibly, matplotlib v1.1+
plt.draw()
plt.show()
#fig.savefig(plot_name, bbox_inches='tight')


##--------------------------------------------------------------------------##
##  Close PostgreSQL database connection
##--------------------------------------------------------------------------##
db_conn.close()



