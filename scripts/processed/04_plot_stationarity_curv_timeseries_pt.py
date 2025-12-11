import sys
utils_dir = '/perm/mofp/era5_curv'
if utils_dir not in sys.path:
    sys.path.append(utils_dir)
import os
import numpy as np
import metview as mv
from scipy.stats import linregress
import matplotlib.pyplot as plt
from utils.paths import DATA_COMPUTE_DIR, DATA_PLOTS_DIR

np.set_printoptions(threshold=sys.maxsize) # to print full numpy arrays (useful for debugging)

###################################################################################################################################
# DESCRIPTION CODE
# 04_plot_stationarity_curv_timeseries_pt.py plots the timeseries of the stationarity of (anti)cyclonic features from the curvature diagnostic for a single point.
# Code runtime: up to 5 minutes.

# DESCRIPTION INPUT PARAMETERS
# year_s (integer, format YYYY): start year to consider.
# year_f (integer, format YYYY): final year to consider.
# radius_list (list of integers, in meters): list of radiuses used in the curvature diagnostic to identify (anti)cyclonic features.
# thr_features_list (list of integers, adimensional): list of thresholds to define the (anti)cyclonic features in the curv diagnostic.
# alpha (float, from 0 to 1): level of significance for the trend lines.
# coord_pt (list of floats): latitude and longitude coordinates of the considered point. 
# name_pt (string): name of the point as "City,Country".
# dir_in (string): relative path of the directory containing the maximum number of days with consecutives (anti)cyclonic features.
# dir_out (string): relative path of the directory containing the timeseries plot of the maximum number of days with consecutives (anti)cyclonic features per year.

# INPUT PARAMETERS
year_s = 1940
year_f = 2023
radius_list = [500, 1000, 2000, 3000]
thr_features_list = [7, 11, 15]
alpha = 0.05
coord_pt = [39.47, -0.37]
name_pt = "Valencia, Spain"
dir_in = os.path.join(DATA_COMPUTE_DIR, "03_stationarity_curv_fields")
dir_out = os.path.join(DATA_PLOTS_DIR, "04_stationarity_curv_timeseries_pt")
###################################################################################################################################


# Plotting the timeseries for a specific curv radius
for radius in radius_list: 

    # Plotting the timeseries for a specific value of curv defining (anti)cyclonic features
    for thr_features in thr_features_list:
        
        dir_in_temp = os.path.join(dir_in, str(radius) + "m_" + str(thr_features) + "curv")
        
        # Plotting the timeseries for a specific for (anti)cyclonic features
        type_feature_list = ["cyclonic", "anticyclonic"]
        type_feature_timeseries_colour_list = ["mediumblue", "orangered"]
        plt.figure(figsize=(20, 8)) # initialise the timeseries plot
        for ind_type_feature in range(len(type_feature_list)):

            type_feature = type_feature_list[ind_type_feature]
            type_feature_timeseries_colour = type_feature_timeseries_colour_list[ind_type_feature]
            max_days_stat_pt = [] # initialising the variable that will contain the timeseries of maximum number of days with consecutives (anti)cyclonic features for all years
            years_list = []

            # Reading the maximum number of timestamps with consecutives (anti)cyclonic features for a specific year
            for year in range(year_s, year_f+1):

                print("Reading the maximum number of timestamps with consecutives (anti)cyclonic features for year = " + str(year) + ", for radius=" + str(radius) + "m and curv>" + str(thr_features))
                file_in_temp = os.path.join(dir_in_temp, type_feature + "_" + str(year) + ".grib")
                if os.path.exists(file_in_temp):
                    max_days_stat = mv.read(file_in_temp)
                    max_days_stat_pt.append(mv.nearest_gridpoint(max_days_stat, coord_pt))
                    years_list.append(year)

            # Computing the trend lines for the timeseries
            x = np.arange(len(years_list))
            slope, intercept, r_value, pvalue, std_err = linregress(x, max_days_stat_pt)
            y_trend = slope * x + intercept

            # Plot the timeseries with its trend line
            if pvalue < alpha:
                if slope > 0:
                    label_trend = f"Significant (at {int(alpha*100)}% level) upward trend, pvalue = {pvalue:.2f}))"
                else:
                    label_trend = f"Significant (at {int(alpha*100)}% level) downward trend, pvalue = {pvalue:.2f}))"
            else:
                label_trend = f"Not significant trend (at {int(alpha*100)}% level, pvalue = {pvalue:.2f})"
            plt.plot(years_list, max_days_stat_pt, color=type_feature_timeseries_colour, lw=3, label = type_feature + " features")
            plt.plot(years_list, y_trend, "--", color=type_feature_timeseries_colour, lw=1, label = label_trend)

        # Completing the timeseries plot    
        plt.title("Maximum n. of consecutive timestamps with (anti)cyclonic features (" + str(radius) + " m and curv>" + str(thr_features) + ") for " + name_pt + " [lat = " + str(coord_pt[0]) + ", lon = " + str(coord_pt[1]) + "]")
        plt.xticks(years_list, rotation=90, fontsize=8)
        plt.legend()

        # Save the timeseries plots
        os.makedirs(dir_out, exist_ok=True)
        city_name = name_pt.split(',')[0]
        country_name = name_pt.split(',')[1]
        plt.savefig(dir_out + "/stationarity_" + str(year_s) + "_" + str(year_f) + "_" + city_name + "_" + country_name + "_" + str(radius) + "m_" + str(thr_features) + "curv.png", dpi=1000, bbox_inches='tight')
        plt.close()