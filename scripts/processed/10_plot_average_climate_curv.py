import sys
utils_dir = '/perm/mofp/era5_curv'
if utils_dir not in sys.path:
    sys.path.append(utils_dir)
import os
import numpy as np
import metview as mv
import matplotlib.pyplot as plt
from utils.paths import ERA5_ECPOINT_TP_24H_DIR, DATA_COMPUTE_DIR, DATA_PLOTS_DIR

np.set_printoptions(threshold=sys.maxsize) # to print full numpy arrays (useful for debugging)


#################################################################################################################
# DESCRIPTION CODE
# 10_plot_average_climate_curv.py plots the average against the climatology for the curv diagnostic, at a specific grid-point.
#Runtime: negligible.

# DESCRIPTION INPUT PARAMETERS
# year_s (integer, format YYYY): start year to consider.
# year_f (integer, format YYYY): final year to consider.
# radius_list (list of integers, adimensional): list of radius used to compute the curv diagnostic.
# dir_in_tp (string): relative path of the directory containing the 24-hourly rainfall reanalysis (ecPoint).
# dir_in_curv (string): relative path of the directory containing the curv diagnostic.
# dir_out (string): relative path of the directory containing the plots of the correlations between the curv diagnostic and 24-hourly rainfall.

# INPUT PARAMETERS
year_s = 1979
year_f = 2024
radius_list = [1000]
season_list = ["DJF", "MAM", "JJA", "SON"]
coord_pt = [39.47, -0.37]
name_pt = "Valencia_Spain"
dir_in_tp = ERA5_ECPOINT_TP_24H_DIR
dir_in_av_curv = os.path.join(DATA_COMPUTE_DIR, "08_average_curv")
dir_in_climate_curv = os.path.join(DATA_COMPUTE_DIR, "09_climate_curv/1991_2020")
dir_out = os.path.join(DATA_PLOTS_DIR, "10_plot_average_climate_curv")
#################################################################################################################


# Plotting the average CURV, against climatology, for a specific radius
for radius in radius_list:

    # Plotting the average CURV, against climatology, for a specific season
    for season in season_list:

        print(" ")

        # Reading the CURV climatology
        curv_climate = mv.read(f"{dir_in_climate_curv}/{radius}/curv_climate_{season}.grib")
        curv_climate_pt = mv.nearest_gridpoint(curv_climate, coord_pt)

        # Reading the average CURV for the analysis period
        curv_av = []
        for year in range(year_s, year_f + 1):
            print(f"Season: {season}, Year: {year} - Curv radius: {radius}")
            curv_av.append( mv.nearest_gridpoint( mv.read(f"{dir_in_av_curv}/{radius}/av_curv_{year}_{season}.grib"), coord_pt ) )

        # Plotting and saving the curv climatology
        plt.plot(np.arange(year_s, year_f + 1), curv_av, color = "crimson", lw = 0.5)
        plt.plot([year_s, year_f], [curv_climate_pt, curv_climate_pt], "--", color = "royalblue", lw = 1)
        plt.plot([year_s - 2, year_f + 2], [0, 0], "--", color = "dimgray", lw = 2)
        plt.xlim([year_s - 2, year_f + 2])
        plt.ylim([-5, 7])

        # Saving the curv climatology plot
        dir_out_temp = f"{dir_out}/{name_pt}/{year_s}_{year_f}"
        os.makedirs(dir_out_temp, exist_ok=True)
        plt.savefig(f"{dir_out_temp}/curv_av_climate_{season}_{radius}m.png", dpi=1000, bbox_inches='tight')
        plt.close()