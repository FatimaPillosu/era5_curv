import sys
utils_dir = '/perm/mofp/era5_curv'
if utils_dir not in sys.path:
    sys.path.append(utils_dir)
import os
import numpy as np
import metview as mv
import matplotlib.pyplot as plt
from utils.paths import DATA_COMPUTE_DIR, DATA_PLOTS_DIR
from utils.definitions import thr_curv_4_ac_features_vals

np.set_printoptions(threshold=sys.maxsize) # to print full numpy arrays (useful for debugging)


############################################################################
# DESCRIPTION CODE
# 13_plot_summary_trend_curv_vals_hist.py plots a histogram about the trend statistics 
# of CURV values for different categories.
#Runtime: ~ 1 minute.

# DESCRIPTION INPUT PARAMETERS
# year_s (integer, format YYYY): start year to consider.
# year_f (integer, format YYYY): final year to consider.
# season_list (list of strings): list of considered seasons.
# radius_list (list of integers, adimensional): list of radius used to compute the curv diagnostic.
# dir_in (string): relative path of the directory containing the average curv diagnostic.
# dir_out (string): relative path of the directory containing the trend plots.

# INPUT PARAMETERS
year_s = 1950
year_f = 2024
season_list = ["JJA", "MAM", "JJA", "SON"]
radius_list = [2000]
dir_in = os.path.join(DATA_COMPUTE_DIR, "11_trend_vals_curv_global")
dir_out = os.path.join(DATA_PLOTS_DIR, "13_summary_trend_curv_vals_hist")
############################################################################


# Plotting the average CURV, against climatology, for a specific season
for season in season_list:

    # Plotting the average CURV, against climatology, for a specific radius
    for radius in radius_list:
        
        print(f"Plotting CURV for season: {season} and  radius: {radius}")

        # Plotting the average number of CURV vals, per category
        for ind_thr_curv in range(len(thr_curv_4_ac_features_vals)-1):
            
            thr_curv_low = thr_curv_4_ac_features_vals[ind_thr_curv]
            thr_curv_up = thr_curv_4_ac_features_vals[ind_thr_curv + 1]
            print(f"    - for thr_curv_low = {thr_curv_low} and thr_curv_up = {thr_curv_up}")

            # Reading the trend statistics
            slope = mv.read(f"{dir_in}/{year_s}_{year_f}/{radius}m/{season}/sen_slope_{thr_curv_low}_{thr_curv_up}.grib")
            pvalue = mv.read(f"{dir_in}/{year_s}_{year_f}/{radius}m/{season}/pvalue_{thr_curv_low}_{thr_curv_up}.grib")
            significant_slope = slope * (pvalue <= 0.05)

            # Plotting summary histogram
            

        exit()            