import sys
utils_dir = '/perm/mofp/era5_curv'
if utils_dir not in sys.path:
    sys.path.append(utils_dir)
import os
import numpy as np
import pandas as pd
import metview as mv
import matplotlib.pyplot as plt
from utils.paths import DATA_RAW_DIR, DATA_PLOTS_DIR
from utils.definitions import thr_curv_4_ac_features_vals, thr_curv_4_ac_features_categories

np.set_printoptions(threshold=sys.maxsize) # to print full numpy arrays (useful for debugging)

#########################################################################################################################
# DESCRIPTION CODE
# 02_plot_curv_timeseries_pt.py computes the stationarity of (anti)cyclonic features from the curvature diagnostic for a single point.
# Code runtime: up to 20 minutes for the whole dataset from 1940 to now.

# DESCRIPTION INPUT PARAMETERS
# year_s (integer, format YYYY): start year to consider.
# year_f (integer, format YYYY): final year to consider.
# radius_list (list of integers, in meters): list of radiuses used in the curvature diagnostic to identify (anti)cyclonic features.
# coord_pt (list of floats): latitude and longitude coordinates of the considered point. 
# name_pt (string): name of the point as "City,Country".
# dir_in (string): relative path of the directory containing the curvature diagnostic.
# dir_out (string): relative path of the directory containing the frequency plots of the number of (anti)cyclonic features created with varying radiuses.

# INPUT PARAMETERS
year_s = 2000
year_f = 2023
radius_list = [500]
coord_pt = [39.23,9.12]
name_pt = "Cagliari,Italy"
dir_in = os.path.join(DATA_RAW_DIR, "era5/curv")
dir_out = os.path.join(DATA_PLOTS_DIR, "02_curv_timeseries_pt")
#########################################################################################################################


# Preparing the x=axis labels for the timeseries plot
years = np.arange(year_s, year_f+1)
dates = pd.date_range(start=str(year_s) + '-01-01', end= str(year_f+1) + '-1-1', freq='6h')[:-1]
selected_dates = []
if (year_f - year_s) < 10:
    for year in years:
        for month in [3, 6, 9, 12]:  # March, June, September, December
            selected_dates.append(pd.Timestamp(year=year, month=month, day=1))
            print_date = '%b-%Y'
            rotation_date = 45
else:
    for year in years:
        for month in [1]:  # March, June, September, December
            selected_dates.append(pd.Timestamp(year=year, month=month, day=1))
            print_date = '%Y'
            rotation_date = 90

# Read the curvature diagnostic for different radiuses
for radius in radius_list:

    # Read the curvature diagnostic for a specific radius and different years
    curv_pt = []
    for year in range(year_s, year_f+1):

        print("Reading the curvature diagnostic for radius = " + str(radius) + " m and year = " + str(year))
        filename_in = "z500_curv" + str(radius) + "_" + str(year) + ".grib"
        file_in = os.path.join(dir_in, filename_in)
        curv = mv.read(file_in)
        curv_pt.extend(mv.nearest_gridpoint(curv, coord_pt))
    
    # Plotting the timeseries for the years considered
    plt.figure(figsize=(30, 12))
    plt.plot(dates, curv_pt, color="teal", lw=0.5)
    plt.plot(dates, np.arange(len(curv_pt))*0 - 7, color="dimgray", lw=2) # edge for mainly anticyclonic features
    plt.plot(dates, np.arange(len(curv_pt))*0 + 7, color="dimgray", lw=2) # edge for mainly cyclonic features
    plt.title("Curv timeseries for " + name_pt + " [lat = " + str(coord_pt[0]) + ", lon = " + str(coord_pt[1]) + "]")
    plt.ylabel("Curv [-]")
    plt.xticks(selected_dates, [date.strftime(print_date) for date in selected_dates], rotation=rotation_date, fontsize=8)
    plt.grid(True, axis='x', linestyle='--', color='gray', alpha=0.5)
    
    # Save the timeseries plots
    os.makedirs(dir_out, exist_ok=True)
    city_name = name_pt.split(',')[0]
    country_name = name_pt.split(',')[1]
    plt.savefig(dir_out + "/timeseries_" + str(year_s) + "_" + str(year_f) + "_" + city_name + "_" + country_name + "_" + str(radius) + ".png", dpi=1000, bbox_inches='tight')
    plt.close()