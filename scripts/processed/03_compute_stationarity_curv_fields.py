import sys
utils_dir = '/perm/mofp/era5_curv'
if utils_dir not in sys.path:
    sys.path.append(utils_dir)
import os
import numpy as np
import metview as mv
from utils.paths import DATA_RAW_DIR, DATA_COMPUTE_DIR

np.set_printoptions(threshold=sys.maxsize) # to print full numpy arrays (useful for debugging)

##########################################################################################################
# DESCRIPTION CODE
# 03_plot_stationarity_curv_fields.py computes the maximum number of stationarity (anti)cyclonic features from the 
# curv diagnostic.
# Code runtime: up to 1 hour.

# DESCRIPTION INPUT PARAMETERS
# year_s (integer, format YYYY): start year to consider.
# year_f (integer, format YYYY): final year to consider.
# radius_list (list of integers, in meters): list of radiuses used in the curvature diagnostic to identify (anti)cyclonic features.
# thr_features_list (list of integers, adimensional): list of thresholds to define the (anti)cyclonic features in the curv diagnostic.
# dir_in (string): relative path of the directory containing the curvature diagnostic.
# dir_out (string): relative path of the directory containing the maximum number of days with consecutives (anti)cyclonic features.

# INPUT PARAMETERS
year_s = 1940
year_f = 2023
radius_list = [500, 1000, 2000, 3000]
thr_features_list = [7, 11, 15]
dir_in = os.path.join(DATA_RAW_DIR, "era5/curv")
dir_out = os.path.join(DATA_COMPUTE_DIR, "03_stationarity_curv_fields")
##########################################################################################################

# COSTUM FUNCTIONS
def max_consecutive_true_in_rows(arr_2d):
    arr_int = arr_2d.astype(int)
    counts = np.zeros_like(arr_int)
    counts[:, 0] = arr_int[:, 0]
    for j in range(1, arr_int.shape[1]):
        counts[:, j] = (counts[:, j-1] + 1) * arr_int[:, j]
    return counts.max(axis=1)

##########################################################################################################


for radius in radius_list: 

    for thr_features in thr_features_list:
        
        # Read the curvature diagnostic for a specific radius and different years
        years_list = np.arange(year_s, year_f+1).astype(int)
        cyclonic_year = []
        anticyclonic_year = []

        for year in range(year_s, year_f+1):

            print("Reading the curvature diagnostic for radius = " + str(radius) + " m, thr_feature = " + str(thr_features) + ", and year = " + str(year))
            
            # Calculating stationarity of (anti)cyclonic features for a certain number of timestamps
            filename_in = "z500_curv" + str(radius) + "_" + str(year) + ".grib"
            file_in = os.path.join(dir_in, filename_in)
            if os.path.exists(file_in):
                
                # Compute the maximum number of consecutive stationary features
                curv_0 = mv.read(file_in)[0:-1]
                curv_1 = mv.read(file_in)[1:]

                stat_cyclonic = mv.values((curv_0 > thr_features) and (curv_1 > thr_features)).astype(bool).T
                max_cons_stat_cyclonic = max_consecutive_true_in_rows(stat_cyclonic)
                max_cons_stat_cyclonic_grib = mv.set_values(curv_0[0], max_cons_stat_cyclonic)

                stat_anticyclonic = mv.values((curv_0 < -thr_features) and (curv_1 < -thr_features)).astype(bool).T
                max_cons_stat_anticyclonic = max_consecutive_true_in_rows(stat_anticyclonic)
                max_cons_stat_anticyclonic_grib = mv.set_values(curv_0[0], max_cons_stat_anticyclonic)

                # Saving the counts as grib files
                dir_out_temp = dir_out + "/" + str(radius) + "m_" + str(thr_features) + "curv" 
                os.makedirs(dir_out_temp, exist_ok=True)
                mv.write(dir_out_temp + "/cyclonic_" + str(year) + ".grib", max_cons_stat_cyclonic_grib)
                mv.write(dir_out_temp + "/anticyclonic_" + str(year) + ".grib", max_cons_stat_anticyclonic_grib)