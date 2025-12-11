import sys
utils_dir = '/perm/mofp/era5_curv'
if utils_dir not in sys.path:
    sys.path.append(utils_dir)
import os
import numpy as np
import metview as mv
from utils.paths import DATA_COMPUTE_DIR, DATA_PLOTS_DIR

np.set_printoptions(threshold=sys.maxsize) # to print full numpy arrays (useful for debugging)

###################################################################################################################################
# DESCRIPTION CODE
# 06_plot_stationarity_curv_trend_stats_global.py plots the statistics for the timeseries trends on the stationarity of (anti)cyclonic features from the curvature
# diagnostic for global fields.
#Runtime: negligible.

# DESCRIPTION INPUT PARAMETERS
# year_s (integer, format YYYY): start year to consider.
# year_f (integer, format YYYY): final year to consider.
# radius_list (list of integers, in meters): list of radiuses used in the curvature diagnostic to identify (anti)cyclonic features.
# thr_features_list (list of integers, adimensional): list of thresholds to define the (anti)cyclonic features in the curv diagnostic.
# dir_in (string): relative path of the directory containing the trend statistics for the maximum number of days with consecutives (anti)cyclonic features per year.
# dir_out (string): relative path of the directory containing the map plots for the trend statistics.

# INPUT PARAMETERS
year_s = 2000
year_f = 2023
radius_list = [500, 1000, 2000, 3000]
thr_features_list = [7, 11, 15]
dir_in = os.path.join(DATA_COMPUTE_DIR, "05_stationarity_curv_trend_stats_global")
dir_out = os.path.join(DATA_PLOTS_DIR, "06_stationarity_curv_trend_stats_global")
###################################################################################################################################


# Reading the trend stats for a specific curv radius
for radius in radius_list: 

    # Reading the trend stats for a specific value of curv defining (anti)cyclonic features
    for thr_features in thr_features_list:
        
        dir_in_temp = os.path.join(dir_in, str(radius) + "m_" + str(thr_features) + "curv")
        
        # Reading the trend stats for a specific for (anti)cyclonic features
        type_feature_list = ["cyclonic", "anticyclonic"]
        colour_type_feature_list = [ ["RGB(0.1098,0.7216,0.651)", "RGB(0.6824,0.451,0.06667)", "RGB(0.9,0.9,0.9)"], ["RGB(1,0,0)", "RGB(0,0,1)", "RGB(0.9,0.9,0.9)"] ]
        for ind_type_feature in range(len(type_feature_list)):

            type_feature = type_feature_list[ind_type_feature]
            colour_type_feature = colour_type_feature_list[ind_type_feature]               

            print("Reading the trend statistics for radius=" + str(radius) + "m, curv>" + str(thr_features) + ", and " + type_feature + " feature")
            file_in_slope = dir_in + "/trend_" + str(year_s) + "_to_" + str(year_f) + "/" + str(radius) + "m_" + str(thr_features) + "curv/slope_" + type_feature + ".grib" 
            file_in_pvalue = dir_in + "/trend_" + str(year_s) + "_to_" + str(year_f) + "/" + str(radius) + "m_" + str(thr_features) + "curv/pvalue_" + type_feature + ".grib" 
            if os.path.exists(file_in_slope) and os.path.exists(file_in_pvalue):
                
                slope = mv.read(file_in_slope)
                trend_upward = mv.bitmap(slope > 0.01, 0) * slope
                trend_downward = mv.bitmap(slope < -0.01, 0) * slope 
                no_trend = mv.bitmap(slope > -0.01 and slope < 0.01, 0) * slope
                pvalue = mv.read(file_in_pvalue)
                
                # Plotting the trend stats
                coastlines = mv.mcoast(
                    map_coastline_colour = "charcoal",
                    map_coastline_thickness = 3,
                    map_coastline_resolution = "medium",
                    map_boundaries = "on",
                    map_boundaries_colour = "charcoal",
                    map_boundaries_thickness = 2,
                    map_grid = "off",
                    map_label = "off"
                    )

                contouring_slope_upward = mv.mcont(
                    legend = "on",
                    contour = "off",
                    contour_level_selection_type = "level_list",
                    contour_level_list = [0.01, 10],
                    contour_label = "off",
                    contour_shade = "on",
                    contour_shade_colour_method = "list",
                    contour_shade_technique     = "grid_shading",
                    contour_shade_colour_list = [colour_type_feature[0]]
                    )

                contouring_slope_downward = mv.mcont(
                    legend = "on",
                    contour = "off",
                    contour_level_selection_type = "level_list",
                    contour_level_list = [-10, -0.01],
                    contour_label = "off",
                    contour_shade = "on",
                    contour_shade_colour_method = "list",
                    contour_shade_technique     = "grid_shading",
                    contour_shade_colour_list = [colour_type_feature[1]]
                    )

                contouring_slope_notrend = mv.mcont(
                    legend = "on",
                    contour = "off",
                    contour_level_selection_type = "level_list",
                    contour_level_list = [-0.01, 0.01],
                    contour_label = "off",
                    contour_shade = "on",
                    contour_shade_colour_method = "list",
                    contour_shade_technique     = "grid_shading",
                    contour_shade_colour_list = [colour_type_feature[2]]
                    )
                
                contouring_pvalue = mv.mcont(
                    legend = "on",
                    contour = "off",
                    contour_level_selection_type = "level_list",
                    contour_level_list = [-0.1, 0.0001, 0.01, 0.05, 0.11],
                    contour_label = "off",
                    contour_shade = "on",
                    contour_shade_colour_method = "list",
                    contour_shade_technique     = "grid_shading",
                    contour_shade_colour_list = ["black", "rgb(0.902,0.2902,0.2235)", "rgb(0.1451,0,1)", "rgb(0,0.549,0.1882)"]
                    )

                legend = mv.mlegend(
                    legend_text_colour = "charcoal",
                    legend_text_font = "arial",
                    legend_text_font_size = 0.3,
                    legend_entry_plot_direction = "row",
                    legend_box_blanking = "on",
                    legend_entry_text_width = 50
                    )

                # Saving the maps
                dir_out_temp = dir_out_temp = dir_out + "/trend_" + str(year_s) + "_to_" + str(year_f) + "/" + str(radius) + "m_" + str(thr_features) + "curv" 
                os.makedirs(dir_out_temp, exist_ok=True)

                file_out_slope = dir_out_temp + "/slope_" + type_feature
                png_slope = mv.png_output(output_width = 5000, output_name = file_out_slope)
                mv.setoutput(png_slope)
                mv.plot(trend_upward, contouring_slope_upward, trend_downward, contouring_slope_downward, no_trend, contouring_slope_notrend, coastlines, legend)

                file_out_pvalue = dir_out_temp + "/pvalue_" + type_feature
                png_pvalue = mv.png_output(output_width = 5000, output_name = file_out_pvalue)
                mv.setoutput(png_pvalue)
                mv.plot(pvalue, contouring_pvalue, coastlines, legend)