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

#np.set_printoptions(threshold=sys.maxsize) # to print full numpy arrays (useful for debugging)


############################################################################
# DESCRIPTION CODE
# 07_plot_trend_pt_radius.py plots the trend for the curv diagnostic for varying radiuses but 
# for a specific grid-point.
#Runtime: ~ 1 minute.

# DESCRIPTION INPUT PARAMETERS
# year_s (integer, format YYYY): start year to consider.
# year_f (integer, format YYYY): final year to consider.
# season_list (list of strings): list of considered seasons.
# radius_list (list of integers, adimensional): list of radius used to compute the curv diagnostic.
# coord_pt (list of floats): list of the lat/lon corrdinates for the considered point.
# name_pt (string): name for the considered point.
# dir_in (string): relative path of the directory containing the average curv diagnostic.
# dir_out (string): relative path of the directory containing the trend plots.

# INPUT PARAMETERS
year_s = 1940
year_f = 2024
season_list = ["DJF", "MAM", "JJA", "SON"]
season_colour_list = ["blue", "green", "yellow", "orange"]
radius_list = [500, 1000, 2000, 3000]
dir_in = os.path.join(DATA_COMPUTE_DIR, "05_trend_global")
dir_out = os.path.join(DATA_PLOTS_DIR, "07_trend_pt_radius")
############################################################################


# Plotting the average CURV, against climatology, for a specific season
for ind_season, season in enumerate(season_list):

    # Plotting the average CURV, against climatology, for a specific radius
    all_slopes_list = []
    significant_trend_list = []
    for radius in radius_list:

        # Reading the trend statistics over the analysis period
        slope = mv.read(f"{dir_in}/{year_s}_{year_f}/sen_slope_{season}_{radius}m.grib")
        pvalue = mv.read(f"{dir_in}/{year_s}_{year_f}/pvalue_{season}_{radius}m.grib")
        significant_slopes =  mv.values( (pvalue <= 0.05) * slope )
        significant_slopes = significant_slopes[significant_slopes != 0]
        all_slopes_list.append(mv.values(slope))
        significant_trend_list.append(significant_slopes)
        
    # Plotting a summary of the trend stastics
    plt.figure(figsize=(6, 4))

    positions_all = np.arange(1, len(radius_list) + 1) - 0.15
    positions_sig = np.arange(1, len(radius_list) + 1) + 0.15

    plt.violinplot(all_slopes_list, positions=positions_all, widths=0.25, showmeans=True, showmedians=False, showextrema=False)
    plt.violinplot(significant_trend_list, positions=positions_sig, widths=0.25, showmeans=True, showmedians=False, showextrema=False)

    x = np.arange(0, len(radius_list) + 2)
    y = x * 0
    plt.plot(x, y, lw=1, color="grey")
    
    plt.xticks(np.arange(1, len(radius_list) + 1), radius_list)
    plt.xlabel("Radius [metres]")
    plt.ylabel("Trend slopes")
    plt.xlim([x[0], x[-1]])
    plt.ylim([-0.12, 0.1])
    
    # # Saving the curv climatology plot
    dir_out_temp = f"{dir_out}/{year_s}_{year_f}"
    os.makedirs(dir_out_temp, exist_ok=True)
    plt.savefig(f"{dir_out_temp}/trend_stats_{season}.png", dpi=1000, bbox_inches='tight')
    plt.close()