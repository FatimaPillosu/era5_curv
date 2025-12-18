import sys
utils_dir = '/perm/mofp/era5_curv'
if utils_dir not in sys.path:
    sys.path.append(utils_dir)
import os
import numpy as np
import pandas as pd
import pymannkendall as mk
import metview as mv
import matplotlib.pyplot as plt
from utils.paths import DATA_COMPUTE_DIR, DATA_PLOTS_DIR

np.set_printoptions(threshold=sys.maxsize) # to print full numpy arrays (useful for debugging)


############################################################################
# DESCRIPTION CODE
# 04_plot_trend_pt.py plots the trend for the curv diagnostic, for a specific grid-points.
#Runtime: ~ 1 minute.

# DESCRIPTION INPUT PARAMETERS
# year_s (integer, format YYYY): start year to consider.
# year_f (integer, format YYYY): final year to consider.
# season_list (list of strings): list of considered seasons.
# radius_list (list of integers, adimensional): list of radius used to compute the curv diagnostic.
# coord_pt (list of floats): list of the lat/lon corrdinates for the considered point.
# name_pt (string): name for the considered point.
# running_mean_frame (integer): number of years to calculate the running mean.
# dir_in (string): relative path of the directory containing the average curv diagnostic.
# dir_out (string): relative path of the directory containing the trend plots.

# INPUT PARAMETERS
year_s = 1950
year_f = 2024
season_list = ["SON"]
radius_list = [2000]
# season_list = ["DJF", "MAM", "JJA", "SON"]
# radius_list = [500, 1000, 2000, 3000]
# coord_pt = [50.43, 7.23]
# name_pt = "Ahrweiler "
# coord_pt = [37.75, -25.67]
# name_pt = "Azzorres"
# coord_pt = [44.701126, 7.095450]
# name_pt = "Pian_del_Re"
coord_pt = [39.47, -0.37]
name_pt = "Valencia_Spain"
running_mean_frame = 5
dir_in = os.path.join(DATA_COMPUTE_DIR, "02_average_curv")
dir_in_climate_curv = os.path.join(DATA_COMPUTE_DIR, "03_climate_curv/1991_2020")
dir_out = os.path.join(DATA_PLOTS_DIR, "04_trend_pt")
############################################################################


# Plotting the average CURV, against climatology, for a specific season
for season in season_list:

    # Plotting the average CURV, against climatology, for a specific radius
    for radius in radius_list:

        # Reading the CURV climatology
        curv_climate = mv.read(f"{dir_in_climate_curv}/{radius}/curv_climate_{season}.grib")
        curv_climate_pt = mv.nearest_gridpoint(curv_climate, coord_pt)

        # Reading the average CURV for the analysis period
        curv_av = []
        year_list = np.arange(year_s, year_f + 1)
        for year in year_list:
            print(f"Season: {season} - Curv radius: {radius} - Year: {year}")
            curv_av.append( mv.nearest_gridpoint( mv.read(f"{dir_in}/{radius}/av_curv_{year}_{season}.grib"), coord_pt ) )

        # Computing the trend
        result = mk.original_test(curv_av)
        pvalue = round(result.p, 3)
        sen_slope = round(result.slope, 3)
        intercept = result.intercept
        trend_vals = sen_slope * np.arange( (year_f - year_s) + 1 ) + intercept
        label_vals = f"slope: {sen_slope} (p-value: {pvalue})"

        # Computing the running mean    
        series = pd.Series(curv_av, index=year_list)
        running_mean_centered = series.rolling(window=running_mean_frame, center=True).mean()

        # Plotting the timeseries and the trend
        plt.figure(figsize=(10, 8))
        #plt.figure(figsize=(2.5, 1.5))
        plt.plot(year_list, curv_av, lw=0.5, color = "royalblue")
        plt.plot(year_list, running_mean_centered, lw=0.5, color = "orangered")
        plt.plot(year_list, trend_vals, "--", lw=1, color = "royalblue", label = label_vals)
        plt.plot([1939, 2026], [curv_climate_pt, curv_climate_pt], color = "fuchsia", lw = 0.5)
        plt.plot([1939, 2026], [0,0], lw = 0.5, color = "dimgray")
        plt.xlim([1939, 2026])
        plt.ylim([-4.1, 6.1])
        
        decades_ticks = np.arange(1940, 2030, 10)
        year_ticks = np.arange(1940, 2025+1, 5)
        plt.gca().set_xticks(decades_ticks)
        plt.gca().set_xticks(year_ticks, minor=True)
        plt.gca().tick_params(axis='x', which='major', labelsize=5)
        plt.gca().tick_params(axis='x', which='minor', length=2)

        curv_major_ticks = np.arange(-4, 6+1, 2)
        curv_minor_ticks = np.arange(-4, 6+1, 1)
        plt.gca().set_yticks(curv_major_ticks)
        plt.gca().set_yticks(curv_minor_ticks, minor=True)
        plt.gca().tick_params(axis='y', which='major', labelsize=5)
        plt.gca().tick_params(axis='y', which='minor', length=2)

        plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.12), frameon=False, fontsize=5)

        plt.show()
        exit()
        
        # Saving the curv climatology plot
        dir_out_temp = f"{dir_out}/{name_pt}/{year_s}_{year_f}"
        os.makedirs(dir_out_temp, exist_ok=True)
        plt.savefig(f"{dir_out_temp}/trend_{season}_{radius}m.png", dpi=1000, bbox_inches='tight')
        plt.close()