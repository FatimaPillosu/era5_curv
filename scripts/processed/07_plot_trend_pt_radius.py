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
year_s = 1950
year_f = 2024
season_list = ["DJF", "MAM", "JJA", "SON"]
radius_list = [500, 1000, 2000, 3000]
coord_pt = [39.47, -0.37]
name_pt = "Valencia_Spain"
dir_in = os.path.join(DATA_COMPUTE_DIR, "02_average_curv")
dir_out = os.path.join(DATA_PLOTS_DIR, "04_trend_pt")
############################################################################


# Plotting the average CURV, against climatology, for a specific season
plt.figure(figsize=(10, 8))
for season in season_list:

    # Plotting the average CURV, against climatology, for a specific radius
    sen_slope = []
    for radius in radius_list:

        # Reading the average CURV for the analysis period
        curv_av = []
        year_list = np.arange(year_s, year_f + 1)
        for year in year_list:
            print(f"Season: {season} - Curv radius: {radius} - Year: {year}")
            curv_av.append( mv.nearest_gridpoint( mv.read(f"{dir_in}/{radius}/av_curv_{year}_{season}.grib"), coord_pt ) )

        # Computing the trend
        result = mk.original_test(curv_av)
        sen_slope.append(round(result.slope, 3))

    # Plotting the timeseries and the trend
    plt.plot(radius_list, sen_slope, lw=1, color = "royalblue", label = season)

plt.legend()
plt.show()
exit()

# Saving the curv climatology plot
dir_out_temp = f"{dir_out}/{name_pt}/{year_s}_{year_f}"
os.makedirs(dir_out_temp, exist_ok=True)
plt.savefig(f"{dir_out_temp}/trend_{season}_{radius}m.png", dpi=1000, bbox_inches='tight')
plt.close()