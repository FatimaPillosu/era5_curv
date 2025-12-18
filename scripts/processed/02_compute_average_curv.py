import sys
utils_dir = '/perm/mofp/era5_curv'
if utils_dir not in sys.path:
    sys.path.append(utils_dir)
import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv
from utils.paths import ERA5_ECPOINT_TP_24H_DIR, DATA_RAW_DIR, DATA_COMPUTE_DIR

np.set_printoptions(threshold=sys.maxsize) # to print full numpy arrays (useful for debugging)


#################################################################################################################
# DESCRIPTION CODE
# 02_compute_average_curv.py computed the yearly average for the curv diagnostic, at each grid-point.
#Runtime: ~ 1.5 hours.

# DESCRIPTION INPUT PARAMETERS
# year_s (integer, format YYYY): start year to consider.
# year_f (integer, format YYYY): final year to consider.
# radius_list (list of integers, adimensional): list of radius used to compute the curv diagnostic.
# dir_in_tp (string): relative path of the directory containing the 24-hourly rainfall reanalysis (ecPoint).
# dir_in_curv (string): relative path of the directory containing the curv diagnostic.
# dir_out (string): relative path of the directory containing the plots of the correlations between the curv diagnostic and 24-hourly rainfall.

# INPUT PARAMETERS
year_s = 1940
year_f = 2024
radius_list = [500, 1000, 2000, 3000]
dir_in_tp = ERA5_ECPOINT_TP_24H_DIR
dir_in_curv = os.path.join(DATA_RAW_DIR, "era5/curv")
dir_out = os.path.join(DATA_COMPUTE_DIR, "02_average_curv")
#################################################################################################################


for radius in radius_list:

    # Setting the output directory
    dir_out_temp = f"{dir_out}/{radius}"
    os.makedirs(dir_out_temp, exist_ok=True)

    # Computing the annual and seasonal averages
    for year in range(year_s, year_f + 1):

        print(f"Year: {year} - Curv radius: {radius}")

        # Reading the curv variable
        curv = mv.read(f"{dir_in_curv}/z500_curv{radius}_{year}.grib")

        # Computing and saving the annual average
        av_curv = mv.mean(curv)
        mv.write(f"{dir_out_temp}/av_curv_{year}_annual.grib", av_curv)

        # Computing and saving the seasonal averages
        date_list = np.array(mv.grib_get_string(curv, "date"), dtype='datetime64[D]')
        
        season = "DJF"
        dates_mask = np.array((date_list >= np.datetime64(f'{year}1201')) & (date_list <= np.datetime64(f'{year}1231')) | (date_list >= np.datetime64(f'{year}0101')) & (date_list < np.datetime64(f'{year}0301')))
        dates_mask = np.where(dates_mask)[0]
        curv_season = curv[dates_mask]
        av_curv_season = mv.mean(curv_season)
        mv.write(f"{dir_out_temp}/av_curv_{year}_{season}.grib", av_curv_season)

        season = "MAM"
        dates_mask = np.array((date_list >= np.datetime64(f'{year}0301')) & (date_list <= np.datetime64(f'{year}0531')))
        dates_mask = np.where(dates_mask)[0]
        curv_season = curv[dates_mask]
        av_curv_season = mv.mean(curv_season)
        mv.write(f"{dir_out_temp}/av_curv_{year}_{season}.grib", av_curv_season)

        season = "JJA"
        dates_mask = np.array((date_list >= np.datetime64(f'{year}0601')) & (date_list <= np.datetime64(f'{year}0831')))
        dates_mask = np.where(dates_mask)[0]
        curv_season = curv[dates_mask]
        av_curv_season = mv.mean(curv_season)
        mv.write(f"{dir_out_temp}/av_curv_{year}_{season}.grib", av_curv_season)

        season = "SON"
        dates_mask = np.array((date_list >= np.datetime64(f'{year}0901')) & (date_list <= np.datetime64(f'{year}1130')))
        dates_mask = np.where(dates_mask)[0]
        curv_season = curv[dates_mask]
        av_curv_season = mv.mean(curv_season)
        mv.write(f"{dir_out_temp}/av_curv_{year}_{season}.grib", av_curv_season)