import sys
utils_dir = '/perm/mofp/era5_curv'
if utils_dir not in sys.path:
    sys.path.append(utils_dir)
import os
import numpy as np
import pymannkendall as mk
import metview as mv
from utils.paths import DATA_COMPUTE_DIR

np.set_printoptions(threshold=sys.maxsize) # to print full numpy arrays (useful for debugging)


############################################################################
# DESCRIPTION CODE
# 05_compute_trend_global.py computes the trend for the curv diagnostic, for a global field.
#Runtime: ~ 3 hours.

# DESCRIPTION INPUT PARAMETERS
# year_s (integer, format YYYY): start year to consider.
# year_f (integer, format YYYY): final year to consider.
# radius_list (list of integers, adimensional): list of radius used to compute the curv diagnostic.
# season_list (list of strings): list of considered seasons.
# dir_in (string): relative path of the directory containing the average curv diagnostic.
# dir_out (string): relative path of the directory containing the trend statistics.

# INPUT PARAMETERS
year_s = 1940
year_f = 2024
radius_list = [500, 1000, 2000, 3000]
season_list = ["DJF", "MAM", "JJA", "SON"]
dir_in = os.path.join(DATA_COMPUTE_DIR, "02_average_curv")
dir_out = os.path.join(DATA_COMPUTE_DIR, "05_trend_global")
############################################################################


# Plotting the average CURV, against climatology, for a specific season
for radius in radius_list:

    # Plotting the average CURV, against climatology, for a specific radius
    for season in season_list:

        # Reading the average CURV for the analysis period
        curv_av = None
        year_list = np.arange(year_s, year_f + 1)
        for year in year_list:
            print(f"Season: {season} - Curv radius: {radius} - Year: {year}")
            curv_av = mv.merge( curv_av, mv.read(f"{dir_in}/{radius}/av_curv_{year}_{season}.grib" ) )
        curv_av = mv.values(curv_av)
        
        # Computing the statistics for the trends, as a global field
        num_grid = curv_av.shape[1]
        pvalue = []
        sen_slope = []
        for i in range(num_grid):
            print(f"Season: {season} - Curv radius: {radius} - Processing grid n. {i}/{num_grid}")
            curv_av_temp = curv_av[:, i]
            result = mk.original_test(curv_av_temp)
            pvalue.append(round(result.p, 3))
            sen_slope.append(round(result.slope, 3))
        
        # Save the trend statistics as grib files
        dir_out_temp = f"{dir_out}/{year_s}_{year_f}"
        os.makedirs(dir_out_temp, exist_ok=True)
        template = mv.read(f"{dir_in}/{radius}/av_curv_{year}_{season}.grib")
        
        curv_vals = np.mean(curv_av, axis = 0)
        curv_vals = mv.set_values(template, curv_vals)
        mv.write(f"{dir_out_temp}/curv_vals_{season}_{radius}m.grib", curv_vals)

        pvalue = np.array(pvalue)
        pvalue = mv.set_values(template, pvalue)
        mv.write(f"{dir_out_temp}/pvalue_{season}_{radius}m.grib", pvalue)

        sen_slope = np.array(sen_slope)
        sen_slope = mv.set_values(template, sen_slope)
        mv.write(f"{dir_out_temp}/sen_slope_{season}_{radius}m.grib", sen_slope)