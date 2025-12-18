import sys
utils_dir = '/perm/mofp/era5_curv'
if utils_dir not in sys.path:
    sys.path.append(utils_dir)
import os
import numpy as np
import metview as mv
from utils.paths import DATA_COMPUTE_DIR, DATA_PLOTS_DIR

np.set_printoptions(threshold=sys.maxsize) # to print full numpy arrays (useful for debugging)


############################################################################
# DESCRIPTION CODE
# 08_plot_summary_trend_map.py plots a summary map about the trend statistics.
#Runtime: ~ 1 minute.

# DESCRIPTION INPUT PARAMETERS
# year_s (integer, format YYYY): start year to consider.
# year_f (integer, format YYYY): final year to consider.
# season_list (list of strings): list of considered seasons.
# radius_list (list of integers, adimensional): list of radius used to compute the curv diagnostic.
# coord_pt (list of floats): list of the lat/lon corrdinates for the considered point.
# name_pt (string): name for the considered point.
# dir_in (string): relative path of the directory containing the average curv diagnostic.
# dir_out (string): relative path of the directory containing the trend plots.

# INPUT PARAMETERS
year_s = 1979
year_f = 2024
season_list = ["DJF", "MAM", "JJA", "SON"]
radius_list = [500, 1000, 2000, 3000]
dir_in = os.path.join(DATA_COMPUTE_DIR, "05_trend_global")
dir_out = os.path.join(DATA_PLOTS_DIR, "08_summary_trend_map")
############################################################################


# Plotting the average CURV, against climatology, for a specific season
for season in season_list:

    # Plotting the average CURV, against climatology, for a specific radius
    count_significant_slope = 0
    for radius in radius_list:

        # Reading the trend statistics over the analysis period
        slope = mv.read(f"{dir_in}/{year_s}_{year_f}/sen_slope_{season}_{radius}m.grib")
        pvalue = mv.read(f"{dir_in}/{year_s}_{year_f}/pvalue_{season}_{radius}m.grib")
        count_significant_slope = count_significant_slope + (pvalue <= 0.05)

    # Plotting the map summarizing the trend stastics
    coastlines = mv.mcoast(
        map_coastline_colour = "rgb(0.6, 0.6, 0.6)",
        map_coastline_thickness = 8,
        map_coastline_resolution = "low",
        map_boundaries = "on",
        map_boundaries_colour = "rgb(0.6, 0.6, 0.6)",
        map_boundaries_thickness = 8,
        map_grid = "on",
        map_grid_thickness = "6",
        map_grid_colour = "rgb(0.6, 0.6, 0.6)",
        map_grid_latitude_reference = 0,
        map_grid_latitude_increment = 30,
        map_grid_longitude_reference = 0,
        map_grid_longitude_increment = 60,
        map_label = "off"
        )
    
    geo_view = mv.geoview(
        map_projection  = "mollweide",
        subpage_frame = "off",
        coastlines = coastlines
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
        contour_level_list = [-0.9, 0.1, 1.1, 2.1, 3.1, 4.1],
        contour_label = "off",
        contour_shade = "on",
        contour_shade_colour_method = "list",
        contour_shade_method = "area_fill",
        contour_shade_colour_list = ["white", "rgb(0.851,0.7176,0.4667)", "rgb(0.9412,0.4745,0.3765)", "rgb(0.4235,0.651,0.1922)", "rgb(0.6157,0.4078,0.9412)"]
        )
    
    # Save the trend statistics as grib files
    dir_out_temp = f"{dir_out}/{year_s}_{year_f}"
    os.makedirs(dir_out_temp, exist_ok=True)
    file_out_slope = f"{dir_out_temp}/trend_{season}"
    png_slope = mv.png_output(output_width = 3000, output_name = file_out_slope)
    mv.setoutput(png_slope)
    mv.plot(
        count_significant_slope, contouring_slope,
        geo_view, 
        legend
        )