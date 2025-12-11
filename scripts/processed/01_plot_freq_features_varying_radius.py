import sys
utils_dir = '/perm/mofp/era5_curv'
if utils_dir not in sys.path:
    sys.path.append(utils_dir)
import os
import numpy as np
import metview as mv
import matplotlib.pyplot as plt
from utils.paths import DATA_RAW_DIR, DATA_PLOTS_DIR
from utils.definitions import thr_curv_4_ac_features_vals, thr_curv_4_ac_features_categories

np.set_printoptions(threshold=sys.maxsize) # to print full numpy arrays (useful for debugging)

#########################################################################################################################
# DESCRIPTION CODE
# 01_plot_freq_features_varying_radius.py plots the frequency of (anti)cyclonic features with varing radius for the curvature diagnostic.
# Code runtime: up to 1 hour.

# DESCRIPTION INPUT PARAMETERS
# year_s (integer, format YYYY): start year to consider.
# year_f (integer, format YYYY): final year to consider.
# radius_list (list of integers, in meters): list of radiuses used in the curvature diagnostic to identify (anti)cyclonic features.
# timestamp_list (list of integers, in hours): list of timestamps to consider.
# dir_in (string): relative path of the directory containing the curvature diagnostic.
# dir_out (string): relative path of the directory containing the frequency plots of the number of (anti)cyclonic features created with varying radiuses.

# INPUT PARAMETERS
year_s = 2001
year_f = 2023
radius_list = [500, 1000, 2000, 3000]
dir_in = os.path.join(DATA_RAW_DIR, "era5/curv")
dir_out = os.path.join(DATA_PLOTS_DIR, "01_freq_features_varying_radius")
#########################################################################################################################


# Read the curvature diagnostic for different radiuses
for radius in radius_list:

    # Initialise the figure containing the frequency plot
    fig, ax = plt.subplots() 

    # Initialise the variable that will store the frequency of (anti)cyclonic features for a specific year and radius
    num_pts = 0
    abs_freq_features_list = np.empty(len(thr_curv_4_ac_features_categories), dtype=float) 
    
    # Read the curvature diagnostic for a specific radius and different years
    for year in range(year_s, year_f+1):

        print("Reading the curvature diagnostic for radius = " + str(radius) + " m and year = " + str(year))
        filename_in = "z500_curv" + str(radius) + "_" + str(year) + ".grib"
        file_in = os.path.join(dir_in, filename_in)
        curv = mv.values(mv.read(file_in)).ravel() # to convert the 2-d array into a 1-d array for simplicity as we are considering all timestamps in the frequencies computation
        num_pts = num_pts + curv.shape[0]

        # Compute the absolute frequency of (anti)cyclonic features for all timestamps over the considered years
        print(" - Computing the absolute frequency of (anti)cyclonic features")
        abs_freq_features_list = abs_freq_features_list + np.histogram(curv, bins=thr_curv_4_ac_features_vals)[0]

    # Compute the relative frequency of (anti)cyclonic features over all timestamps and considered years
    rel_freq_features_list = abs_freq_features_list / num_pts * 100

    # Plot the average relative frequency of (anti)cyclonic features over all timestamps and considered years
    plt.barh( thr_curv_4_ac_features_categories, rel_freq_features_list/rel_freq_features_list*100, color="gainsboro" )
    plt.barh( thr_curv_4_ac_features_categories, rel_freq_features_list, color="crimson" )

    ax.set_title("Radius = " + str(radius) + " m", fontsize=10, color='black')
    ax.set_xlabel('%', fontsize=8, color='black')
    ax.set_xlim(-2, 102)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', colors='black', which='both', length=0)
    ax.tick_params(axis='x', colors='black')
    plt.xticks(fontsize=8) 
    plt.yticks(fontsize=8) 
    plt.tight_layout()
    
    # Save the frequency plots
    os.makedirs(dir_out, exist_ok=True)
    plt.savefig(dir_out + "/radius_" + str(radius) + ".png", dpi=500, bbox_inches='tight')