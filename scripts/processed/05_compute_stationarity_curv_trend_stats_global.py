import sys
utils_dir = '/perm/mofp/era5_curv'
if utils_dir not in sys.path:
    sys.path.append(utils_dir)
import os
import numpy as np
import metview as mv
from scipy.stats import linregress
from utils.paths import DATA_COMPUTE_DIR

np.set_printoptions(threshold=sys.maxsize) # to print full numpy arrays (useful for debugging)

###################################################################################################################################
# DESCRIPTION CODE
# 05_compute_stationarity_curv_trend_stats_globl.py computes the statistics for the timeseries trends on the stationarity of (anti)cyclonic features from the 
# curvature diagnostic for global fields.
# Code runtime: up to 1 hour.

# DESCRIPTION INPUT PARAMETERS
# year_s (integer, format YYYY): start year to consider.
# year_f (integer, format YYYY): final year to consider.
# radius_list (list of integers, in meters): list of radiuses used in the curvature diagnostic to identify (anti)cyclonic features.
# thr_features_list (list of integers, adimensional): list of thresholds to define the (anti)cyclonic features in the curv diagnostic.
# dir_in (string): relative path of the directory containing the maximum number of days with consecutives (anti)cyclonic features.
# dir_out (string): relative path of the directory containing the trend statistics for the maximum number of days with consecutives (anti)cyclonic features per year.

# INPUT PARAMETERS
year_s = 2000
year_f = 2023
radius_list = [500, 1000, 2000, 3000]
thr_features_list = [7, 11, 15]
dir_in = os.path.join(DATA_COMPUTE_DIR, "03_stationarity_curv_fields")
dir_out = os.path.join(DATA_COMPUTE_DIR, "05_stationarity_curv_trend_stats_global")
###################################################################################################################################


# Plotting the timeseries for a specific curv radius
for radius in radius_list: 

    # Plotting the timeseries for a specific value of curv defining (anti)cyclonic features
    for thr_features in thr_features_list:
        
        dir_in_temp = os.path.join(dir_in, str(radius) + "m_" + str(thr_features) + "curv")
        
        # Plotting the timeseries for a specific for (anti)cyclonic features
        type_feature_list = ["cyclonic", "anticyclonic"]
        for type_feature in type_feature_list:

            # Reading the maximum number of timestamps with consecutives (anti)cyclonic features for specific years
            max_days_stat = None # initialising the variable that will contain the timeseries of maximum number of days with consecutives (anti)cyclonic features for all years
            years_list = []
            for year in range(year_s, year_f+1):
                print("Reading the maximum number of timestamps with consecutives (anti)cyclonic features for year = " + str(year) + ", for radius=" + str(radius) + "m and curv>" + str(thr_features))
                file_in_temp = os.path.join(dir_in_temp, type_feature + "_" + str(year) + ".grib")
                if os.path.exists(file_in_temp):
                    max_days_stat = mv.merge(max_days_stat, mv.read(file_in_temp))
                    years_list.append(year)

            # Computing the trend lines for the timeseries for each point in the global fields
            max_days_stat = mv.values(max_days_stat)
            slope = []
            pvalue = []
            for i in range(max_days_stat.shape[1]):
                print("Computing stats fro trend lines for grid-point n." + str(i) + "/" + str(max_days_stat.shape[1]))
                x = np.arange(len(years_list))
                slope_pt, _, _, pvalue_pt, _ = linregress(x, max_days_stat[:,i])
                slope.append(slope_pt)
                pvalue.append(pvalue_pt)
            template = mv.read(file_in_temp)
            slope = mv.set_values(template, np.array(slope))
            pvalue = mv.set_values(template, np.array(pvalue))

            # Saving the counts as grib files
            dir_out_temp = dir_out + "/trend_" + str(year_s) + "_to_" + str(year_f) + "/" + str(radius) + "m_" + str(thr_features) + "curv" 
            os.makedirs(dir_out_temp, exist_ok=True)
            mv.write(dir_out_temp + "/slope_" + type_feature + ".grib", slope)
            mv.write(dir_out_temp + "/pvalue_" + type_feature + ".grib", pvalue)