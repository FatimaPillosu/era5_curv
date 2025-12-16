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
dir_out = os.path.join(DATA_PLOTS_DIR, "13_trend_global")
############################################################################


# Plotting the average CURV, against climatology, for a specific season
for radius in radius_list:

    # Plotting the average CURV, against climatology, for a specific radius
    for season in season_list:

        print(f"Plotting the trend statistics for {season} and curv radius = {radius}m")

        # Reading the trend statistics
        curv_vals = mv.read(f"{dir_in}/{year_s}_{year_f}/curv_vals_{season}_{radius}m.grib")
        pvalue = mv.read(f"{dir_in}/{year_s}_{year_f}/pvalue_{season}_{radius}m.grib")
        sen_slope = mv.read(f"{dir_in}/{year_s}_{year_f}/sen_slope_{season}_{radius}m.grib")

        # Defining the cases to plot
        mask_cyclonic_upward = (curv_vals > 0.01) & (sen_slope > 0.005) 
        mask_cyclonic_downward = (curv_vals > 0.01) & (sen_slope < -0.005)
        mask_acyclonic_upward = (curv_vals < -0.01) & (sen_slope > 0.005) 
        mask_acyclonic_downward = (curv_vals < -0.01) & (sen_slope < -0.005)

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
        
        contouring_cyclonic_upward = mv.mcont(
            legend = "on",
            contour = "off",
            contour_level_selection_type = "level_list",
            contour_level_list = [0.9, 1.1],
            contour_label = "off",
            contour_shade = "on",
            contour_shade_colour_method = "list",
            contour_shade_technique     = "grid_shading",
            contour_shade_colour_list = ["rgb(0.28,0.8415,0.776)"]
            )
            
        contouring_cyclonic_downward = mv.mcont(
            legend = "on",
            contour = "off",
            contour_level_selection_type = "level_list",
            contour_level_list = [0.9, 1.1],
            contour_label = "off",
            contour_shade = "on",
            contour_shade_colour_method = "list",
            contour_shade_technique     = "grid_shading",
            contour_shade_colour_list = ["rgb(0.7825,0.9429,0.9242)"]
            )
        
        contouring_acyclonic_upward = mv.mcont(
            legend = "on",
            contour = "off",
            contour_level_selection_type = "level_list",
            contour_level_list = [0.9, 1.1],
            contour_label = "off",
            contour_shade = "on",
            contour_shade_colour_method = "list",
            contour_shade_technique     = "grid_shading",
            contour_shade_colour_list = ["rgb(0.9478,0.3698,0.6588)"]
            )
            
        contouring_acyclonic_downward = mv.mcont(
            legend = "on",
            contour = "off",
            contour_level_selection_type = "level_list",
            contour_level_list = [0.9, 1.1],
            contour_label = "off",
            contour_shade = "on",
            contour_shade_colour_method = "list",
            contour_shade_technique     = "grid_shading",
            contour_shade_colour_list = ["rgb(0.947,0.7236,0.8353)"]
            )
        
        contouring_pvalue_005 = mv.mcont(
            legend = "on",
            contour = "on",
            contour_line_colour = "blue",
            contour_line_thickness = 8,
            contour_line_style = "solid",
            contour_label = "off",
            contour_highlight = "off",
            contour_max_level = 0.05,
            contour_min_level = 0.05,
            contour_level_count = 1
        )

        # Save the trend statistics as grib files
        dir_out_temp = f"{dir_out}/{year_s}_{year_f}"
        os.makedirs(dir_out_temp, exist_ok=True)
        file_out_slope = f"{dir_out_temp}/trend_{season}_{radius}m"
        png_slope = mv.png_output(output_width = 3000, output_name = file_out_slope)
        mv.setoutput(png_slope)
        mv.plot(mask_cyclonic_upward, contouring_cyclonic_upward, 
                mask_cyclonic_downward, contouring_cyclonic_downward,
                mask_acyclonic_upward, contouring_acyclonic_upward, 
                mask_acyclonic_downward, contouring_acyclonic_downward,
                pvalue, contouring_pvalue_005,
                coastlines, legend
                )