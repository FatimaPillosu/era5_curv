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
# 09_compute_climate_curv.py computed the climatology for the curv diagnostic, at each grid-point.
#Runtime: ~ 1 minute.

# DESCRIPTION INPUT PARAMETERS
# year_s (integer, format YYYY): start year to consider.
# year_f (integer, format YYYY): final year to consider.
# radius_list (list of integers, adimensional): list of radius used to compute the curv diagnostic.
# dir_in_tp (string): relative path of the directory containing the 24-hourly rainfall reanalysis (ecPoint).
# dir_in_curv (string): relative path of the directory containing the curv diagnostic.
# dir_out (string): relative path of the directory containing the plots of the correlations between the curv diagnostic and 24-hourly rainfall.

# INPUT PARAMETERS
year_s = 1991
year_f = 2020
radius_list = [500, 1000, 2000, 3000]
dir_in = os.path.join(DATA_COMPUTE_DIR, "08_average_curv")
dir_out = os.path.join(DATA_COMPUTE_DIR, "09_climate_curv")
#################################################################################################################


for radius in radius_list:

    # Setting the output directory
    dir_out_temp = f"{dir_out}/{year_s}_{year_f}/{radius}"
    os.makedirs(dir_out_temp, exist_ok=True)

    # Computing the annual and seasonal climatologies
    curv_climate_year = None
    curv_climate_DJF = None
    curv_climate_MAM = None
    curv_climate_JJA = None
    curv_climate_SON = None
    for year in range(year_s, year_f + 1):

        print(f"Year: {year} - Curv radius: {radius}")

        curv_climate_year = mv.merge(curv_climate_year, mv.read(f"{dir_in}/{radius}/av_curv_{year}_annual.grib"))
        curv_climate_DJF = mv.merge(curv_climate_DJF, mv.read(f"{dir_in}/{radius}/av_curv_{year}_DJF.grib"))
        curv_climate_MAM = mv.merge(curv_climate_MAM, mv.read(f"{dir_in}/{radius}/av_curv_{year}_MAM.grib"))
        curv_climate_JJA = mv.merge(curv_climate_JJA, mv.read(f"{dir_in}/{radius}/av_curv_{year}_JJA.grib"))
        curv_climate_SON = mv.merge(curv_climate_SON, mv.read(f"{dir_in}/{radius}/av_curv_{year}_SON.grib"))
    
    curv_climate_year = mv.mean(curv_climate_year)
    curv_climate_DJF = mv.mean(curv_climate_DJF)
    curv_climate_MAM = mv.mean(curv_climate_MAM)
    curv_climate_JJA = mv.mean(curv_climate_JJA)
    curv_climate_SON = mv.mean(curv_climate_SON)

    # Saving the output files
    mv.write(f"{dir_out_temp}/curv_climate_annual.grib", curv_climate_year)
    mv.write(f"{dir_out_temp}/curv_climate_DJF.grib", curv_climate_DJF)
    mv.write(f"{dir_out_temp}/curv_climate_MAM.grib", curv_climate_MAM)
    mv.write(f"{dir_out_temp}/curv_climate_JJA.grib", curv_climate_JJA)
    mv.write(f"{dir_out_temp}/curv_climate_SON.grib", curv_climate_SON)