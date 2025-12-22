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
from utils.definitions import thr_curv_4_ac_features_vals

np.set_printoptions(threshold=sys.maxsize) # to print full numpy arrays (useful for debugging)


############################################################################
# DESCRIPTION CODE
# 10_plot_trend_vals_curv.py plots the trend for the curv diagnostic, for a global field.
#Runtime: ~ 1 minute.

# DESCRIPTION INPUT PARAMETERS
# year_s (integer, format YYYY): start year to consider.
# year_f (integer, format YYYY): final year to consider.
# radius_list (list of integers, adimensional): list of radius used to compute the curv diagnostic.
# season_list (list of strings): list of considered seasons.
# coord_pt (list of floats): list of the lat/lon corrdinates for the considered point.
# name_pt (string): name for the considered point.
# dir_in (string): relative path of the directory containing the average curv diagnostic.
# dir_out (string): relative path of the directory containing the trend plots.

# INPUT PARAMETERS
year_s = 1940
year_f = 1945
radius_list = [3000]
season_list = ["DJF", "MAM", "JJA", "SON"]
coord_pt = [50.43, 7.23]
name_pt = "Ahrweiler "
dir_in = os.path.join(DATA_COMPUTE_DIR, "09_number_days_curv_vals")
dir_out = os.path.join(DATA_PLOTS_DIR, "10_plot_trend_vals_curv")
############################################################################


# Plotting the average number of CURV vals, per category, for a specific radius
for radius in radius_list:

    # Plotting the average number of CURV vals, per category, for a specific season
    for season in season_list:

      print(f"Plotting the trend statistics for {season} and curv radius = {radius}m")

      # Plotting the average number of CURV vals, per category
      for ind_thr_curv in range(len(thr_curv_4_ac_features_vals)-1):
            
            thr_curv_low = thr_curv_4_ac_features_vals[ind_thr_curv]
            thr_curv_up = thr_curv_4_ac_features_vals[ind_thr_curv + 1]
            print(f"    - thr_curv_low = {thr_curv_low} and thr_curv_up = {thr_curv_up}")

            # Reading the count of days of CURV vals within a specific category, for the whole considered period
            year_list = np.arange(year_s, year_f + 1)
            curv_vals = []
            for year in year_list:
                  curv_vals.append( mv.nearest_gridpoint(mv.read(f"{dir_in}/{radius}/{year}/av_curv_{year}_{season}_{thr_curv_low}_{thr_curv_up}.grib"), coord_pt) )

            # Computing the trend statistics
            result = mk.original_test(curv_vals)
            pvalue = round(result.p, 3)
            sen_slope = round(result.slope, 3)
            intercept = result.intercept
            trend_vals = sen_slope * np.arange( (year_f - year_s) + 1 ) + intercept
            label_vals = f"slope: {sen_slope} (p-value: {pvalue})"

            # Computing the running mean    
            series = pd.Series(curv_vals, index=year_list)
            running_mean_centered = series.rolling(window=5, center=True).mean()

            # Plotting the trend stats
            plt.figure(figsize=(10, 8))
            plt.plot(year_list, curv_vals, lw=0.5, color = "royalblue")
            plt.plot(year_list, running_mean_centered, lw=0.5, color = "orangered")
            plt.plot(year_list, trend_vals, "--", lw=1, color = "royalblue", label = label_vals)
            plt.xlim([1939, 2026])
            plt.ylim([0,300])

            decades_ticks = np.arange(1940, 2030, 10)
            year_ticks = np.arange(1940, 2025+1, 5)
            plt.gca().set_xticks(decades_ticks)
            plt.gca().set_xticks(year_ticks, minor=True)
            plt.gca().tick_params(axis='x', which='major', labelsize=5)
            plt.gca().tick_params(axis='x', which='minor', length=2)

            curv_major_ticks = np.arange(0, 300+1, 50)
            curv_minor_ticks = np.arange(0, 300+1, 10)
            plt.gca().set_yticks(curv_major_ticks)
            plt.gca().set_yticks(curv_minor_ticks, minor=True)
            plt.gca().tick_params(axis='y', which='major', labelsize=5)
            plt.gca().tick_params(axis='y', which='minor', length=2)

            plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.12), frameon=False, fontsize=5)

            plt.show()

      exit()