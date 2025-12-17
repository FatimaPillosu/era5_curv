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
# 13_plot_trend_global.py plots the trend for the curv diagnostic, for a global field.
#Runtime: ~ 1 minute.

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
dir_in = os.path.join(DATA_COMPUTE_DIR, "12_trend_global")
dir_out = os.path.join(DATA_PLOTS_DIR, "13_trend_global_new1")
############################################################################


# Plotting the average CURV, against climatology, for a specific season
for radius in radius_list:

    # Plotting the average CURV, against climatology, for a specific radius
    for season in season_list:

        print(f"Plotting the trend statistics for {season} and curv radius = {radius}m")

        # Reading the trend statistics
        sen_slope = mv.read(f"{dir_in}/{year_s}_{year_f}/sen_slope_{season}_{radius}m.grib")
        curv_vals = mv.read(f"{dir_in}/{year_s}_{year_f}/curv_vals_{season}_{radius}m.grib")
        pvalue = mv.read(f"{dir_in}/{year_s}_{year_f}/pvalue_{season}_{radius}m.grib")

        # Selecting slope values where p-value <= 0.05
        significant_slope = sen_slope * (pvalue <= 0.05)

        # Plotting the trend stats
        coastlines = mv.mcoast(
            map_coastline_colour = "charcoal",
            map_coastline_thickness = 4,
            map_coastline_resolution = "low",
            map_boundaries = "on",
            map_boundaries_colour = "charcoal",
            map_boundaries_thickness = 4,
            map_grid = "on",
            map_grid_thickness = "6",
            map_grid_colour = "charcoal",
            map_grid_latitude_reference = 0,
            map_grid_latitude_increment = 30,
            map_grid_longitude_reference = 0,
            map_grid_longitude_increment = 60,
            map_label = "on",
            map_label_colour = "charcoal"
            )
            
        legend = mv.mlegend(
            legend_text_colour = "charcoal",
            legend_text_font = "arial",
            legend_text_font_size = 0.3,
            legend_entry_plot_direction = "row",
            legend_box_blanking = "on",
            legend_entry_text_width = 50
            )
            
        contouring_slope = mv.mcont(
            legend = "on",
            contour = "off",
            contour_level_selection_type = "level_list",
            contour_level_list = [-0.1, -0.02, -0.01, -0.001, 0.001, 0.01, 0.02, 0.1],
            contour_label = "off",
            contour_shade = "on",
            contour_shade_colour_method = "list",
            contour_shade_technique     = "grid_shading",
            contour_shade_colour_list = ["rgb(0.5929,0.4744,0.2541)", "rgb(0.851,0.7176,0.4667)", "rgb(0.947,0.8716,0.7314)", "white", "rgb(0.6079,0.9137,0.878)", "rgb(0.1098,0.7216,0.651)", "rgb(0.2338,0.5506,0.5136)"]
            )
        
        contouring_curv = mv.mcont(
            legend = "on",
            contour_label = "off",
            contour_level_selection_type = "level_list",
            contour_level_list = [-6,-3,0,3,6],
            contour_line_colour_rainbow = "on",
            contour_line_colour_rainbow_method = "list",
            contour_line_colour_rainbow_colour_list = ["rgb(0.6129,0.03026,0.3216)", "rgb(1,0,0.498)", "black", "rgb(0.2825,0.3724,0.9567)", "rgb(0.03148,0.1162,0.6666)"],
            contour_line_thickness_rainbow_list = [8,8,10,8,8]
            )
        
        contouring_curv = mv.mcont(
            legend = "on",
            contour_label = "off",
            contour_level_selection_type = "level_list",
            contour_level_list = [-3,0,3],
            contour_line_colour_rainbow = "on",
            contour_line_colour_rainbow_method = "list",
            contour_line_colour_rainbow_colour_list = ["rgb(1,0,0.498)", "black", "rgb(0,0,1)"],
            contour_line_thickness_rainbow_list = [10,10,10]
            )

        # Save the trend statistics as grib files
        dir_out_temp = f"{dir_out}/{year_s}_{year_f}"
        os.makedirs(dir_out_temp, exist_ok=True)
        file_out_slope = f"{dir_out_temp}/trend_{season}_{radius}m"
        png_slope = mv.png_output(output_width = 3000, output_name = file_out_slope)
        mv.setoutput(png_slope)
        mv.plot(
            significant_slope, contouring_slope,
            curv_vals, contouring_curv,
            coastlines, legend
            )