import sys
utils_dir = '/perm/mofp/era5_curv'
if utils_dir not in sys.path:
    sys.path.append(utils_dir)
import os
import numpy as np
import pymannkendall as mk
import metview as mv
from utils.paths import DATA_COMPUTE_DIR
from utils.definitions import thr_curv_4_ac_features_vals

np.set_printoptions(threshold=sys.maxsize) # to print full numpy arrays (useful for debugging)


############################################################################
# DESCRIPTION CODE
# 11_compute_trend_vals_curv_global.py computes the trend statistics for CURV values, for 
# a global field.
#Runtime: ~ 6 hours.

# DESCRIPTION INPUT PARAMETERS
# year_s (integer, format YYYY): start year to consider.
# year_f (integer, format YYYY): final year to consider.
# radius_list (list of integers, adimensional): list of radius used to compute the curv diagnostic.
# season_list (list of strings): list of considered seasons.
# dir_in (string): relative path of the directory containing the average curv diagnostic.
# dir_out (string): relative path of the directory containing the trend plots.

# INPUT PARAMETERS
year_s = 1950
year_f = 2024
radius_list = [500, 1000, 2000, 3000]
season_list = ["DJF", "MAM", "JJA", "SON"]
dir_in = os.path.join(DATA_COMPUTE_DIR, "09_number_days_curv_vals")
dir_out = os.path.join(DATA_COMPUTE_DIR, "11_trend_vals_curv_global")
############################################################################


# Plotting the average number of CURV vals, per category, for a specific radius
for radius in radius_list:

    # Plotting the average number of CURV vals, per category, for a specific season
    for season in season_list:

      # Plotting the average number of CURV vals, per category
      for ind_thr_curv in range(len(thr_curv_4_ac_features_vals)-1):
            
            thr_curv_low = thr_curv_4_ac_features_vals[ind_thr_curv]
            thr_curv_up = thr_curv_4_ac_features_vals[ind_thr_curv + 1]
            print(f"    - thr_curv_low = {thr_curv_low} and thr_curv_up = {thr_curv_up}")

            # Reading the count of days of CURV vals within a specific category, for the whole considered period
            year_list = np.arange(year_s, year_f + 1)
            curv_vals = None
            for year in year_list:
                  curv_vals = mv.merge( curv_vals,  mv.read(f"{dir_in}/{radius}/{year}/av_curv_{year}_{season}_{thr_curv_low}_{thr_curv_up}.grib") )
            curv_vals = mv.values(curv_vals)

            # Computing the trend statistics
            num_grid = curv_vals.shape[1]
            pvalue = []
            sen_slope = []
            for i in range(num_grid):
                 print(f"Season: {season} - Curv radius: {radius} - Processing grid n. {i}/{num_grid}")
                 curv_vals_temp = curv_vals[:, i]
                 result = mk.original_test(curv_vals_temp)
                 pvalue.append(round(result.p, 3))
                 sen_slope.append(round(result.slope, 3))

            # Save the trend statistics as grib files
            dir_out_temp = f"{dir_out}/{year_s}_{year_f}/{radius}m/{season}"
            os.makedirs(dir_out_temp, exist_ok=True)
            template = mv.read(f"{dir_in}/{radius}/{year}/av_curv_{year}_{season}_{thr_curv_low}_{thr_curv_up}.grib")

            pvalue = np.array(pvalue)
            pvalue = mv.set_values(template, pvalue)
            mv.write(f"{dir_out_temp}/pvalue_{thr_curv_low}_{thr_curv_up}.grib", pvalue)

            sen_slope = np.array(sen_slope)
            sen_slope = mv.set_values(template, sen_slope)
            mv.write(f"{dir_out_temp}/sen_slope_{thr_curv_low}_{thr_curv_up}.grib", sen_slope)