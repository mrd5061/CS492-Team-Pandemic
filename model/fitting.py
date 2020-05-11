#!/usr/bin/env python
# vim: set fileencoding=utf-8 ts=4 sts=4 sw=4 et tw=80 :
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
import matplotlib.pyplot as plt
import pandas as pd
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


# Load data:
base_csv_dir = '../datasets/'
cumu_csv_dir = os.path.join(base_csv_dir, 'csse_covid_19_daily_reports')
time_csv_dir = os.path.join(base_csv_dir, 'csse_covid_19_time_series')
#prefix = 'time_series_19-covid'
#csv_files = sorted(glob.glob('%s/*.csv' % time_csv_dir))
data = {}
#csv_names = ['Confirmed', 'Deaths', 'Recovered']
csv_names = ['confirmed', 'deaths', 'recovered']
# for cname in csv_names:
#     #cbase = 'time_series_19-covid-%s.csv' % cname
#     #cbase = 'time_series_covid19_%s.csv' % cname
#     cbase = 'time_series_covid19_%s_global.csv' % cname
#     cpath = os.path.join(time_csv_dir, cbase)
#     #tag = cname.lower()
#     #cbase = os.path.basename(cfile)
#     #sys.stderr.write("cbase: %s\n" % cbase)
#     sys.stderr.write("cpath: %s\n" % cpath)
#     data[cname] = pd.read_csv(cpath)


data['confirmed'] = pd.read_csv("../datasets/time_series_covid19_confirmed_US_04_20_2020.csv")
data['deaths'] = pd.read_csv("../datasets/time_series_covid19_deaths_US_04_20_2020.csv")


case = data['confirmed']

number_cols = slice(11, None, None)
date_strings = case.keys()[number_cols]


def timefix(when):
    mm, dd, yy = (int(x) for x in when.split('/'))
    return dt.datetime(2000+yy, mm, dd)

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

county_data = case[case[state_col] == which_state]

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

#T_scale = 74.


nyc_days = 42.
nyc_cinf = 0.05
TT, SS, II, RR = model.infect(maxT=5, nsteps=100000) #, transm=5)
all_confirmed = 1.0-SS
pSS = SS*population
pII = II*population
pRR = RR*population
all_confirmed *= population

which = argnear(1.-SS, nyc_cinf)
sirtime = TT[argnear(1.-SS, nyc_cinf)]
T_scale = nyc_days / sirtime
T_scale *= 0.8
T_start += 2
pTT = T_scale*TT + T_start

print("Using T_start=%.2f and T_scale=%.3f." % (T_start, T_scale))

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

ax1.set_yscale('log')
ax1.set_ylim(ymin=0.5)
## Disable axis offsets:
#ax1.xaxis.get_major_formatter().set_useOffset(False)
#ax1.yaxis.get_major_formatter().set_useOffset(False)

#ax1.plot(kde_pnts, kde_vals)
#ax1.scatter(timestamp.jd, country_dead)
#ax1.scatter(fitme_jdutc, fitme_ndead)
ax1.scatter(days_elapsed, total_per_date, lw=0, s=15)

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







