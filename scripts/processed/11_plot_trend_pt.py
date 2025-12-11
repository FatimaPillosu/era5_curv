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
# 11_plot_trend_pt.py plots the trend for the curv diagnostic, for a specific grid-points.
#Runtime: negligible.

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
season_list = ["DJF", "MAM", "JJA", "SON"]
radius_list = [1000]
coord_pt = [39.47, -0.37]
name_pt = "Valencia_Spain"
running_mean_frame = 5
dir_in = os.path.join(DATA_COMPUTE_DIR, "08_average_curv")
dir_in_climate_curv = os.path.join(DATA_COMPUTE_DIR, "09_climate_curv/1991_2020")
dir_out = os.path.join(DATA_PLOTS_DIR, "11_trend_pt")
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
            print(f"Year: {year} - Curv radius: {radius}")
            curv_av.append( mv.nearest_gridpoint( mv.read(f"{dir_in}/{radius}/av_curv_{year}_{season}.grib"), coord_pt ) )

        # Computing the running mean    
        series = pd.Series(curv_av, index=year_list)
        running_mean_centered = series.rolling(window=running_mean_frame, center=True).mean()

        # Computing the trend
        result = mk.original_test(curv_av)
        pvalue = round(result.p, 3)
        sen_slope = round(result.slope, 3)
        intercept = result.intercept
        trend_vals = sen_slope * np.arange( (year_f - year_s) + 1 ) + intercept
        label_vals = f"slope: {sen_slope}\n(p-value: {pvalue})"

        result = mk.original_test(running_mean_centered)
        pvalue = round(result.p, 3)
        sen_slope = round(result.slope, 3)
        intercept = result.intercept
        trend_rm = sen_slope * np.arange( (year_f - year_s) + 1 ) + intercept
        label_rm = f"slope: {sen_slope}\n(p-value: {pvalue})"

        # Plotting the timeseries and the trend
        plt.figure(figsize=(2.8, 2))
        plt.plot(year_list, curv_av, lw=0.3, color = "royalblue")
        plt.plot(year_list, running_mean_centered, lw=0.3, color = "orangered")
        plt.plot(year_list, trend_vals, "--", lw=1, color = "royalblue", label = label_vals)
        plt.plot(year_list, trend_rm, "--", lw=1, color = "orangered", label = label_rm)
        plt.plot([1935, 2030], [curv_climate_pt, curv_climate_pt], linestyle = "dashdot", color = "green", lw = 1)
        plt.plot([1935, 2030], [0,0], lw = 0.5, color = "dimgray")
        plt.xlim([1935, 2030])
        plt.ylim([-3, 6.1])
        plt.xticks(fontsize=6)
        plt.yticks(fontsize=6)
        plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.19), ncol=2, frameon=False, fontsize=6)
        
        # Saving the curv climatology plot
        dir_out_temp = f"{dir_out}/{name_pt}/{year_s}_{year_f}"
        os.makedirs(dir_out_temp, exist_ok=True)
        plt.savefig(f"{dir_out_temp}/curv_av_climate_{season}_{radius}m.png", dpi=1000, bbox_inches='tight')
        plt.close()