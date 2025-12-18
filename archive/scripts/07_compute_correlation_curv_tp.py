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
# 07_compute_correlation_curv_tp.py computed the correlation between the values of the curv diagnostic and rainfall (ecPoint).
#Runtime: negligible.

# DESCRIPTION INPUT PARAMETERS
# year_s (integer, format YYYY): start year to consider.
# year_f (integer, format YYYY): final year to consider.
# radius_list (list of integers, adimensional): list of radius used to compute the curv diagnostic.
# dir_in_tp (string): relative path of the directory containing the 24-hourly rainfall reanalysis (ecPoint).
# dir_in_curv (string): relative path of the directory containing the curv diagnostic.
# dir_out (string): relative path of the directory containing the plots of the correlations between the curv diagnostic and 24-hourly rainfall.

# INPUT PARAMETERS
year_s = 1950
year_f = 2023
radius_list = [1000, 2000, 500, 3000]
dir_in_tp = ERA5_ECPOINT_TP_24H_DIR
dir_in_curv = os.path.join(DATA_RAW_DIR, "era5/curv")
dir_out = os.path.join(DATA_COMPUTE_DIR, "07_compute_correlation_curv_tp")
#################################################################################################################


# Reading the curv values and the corresponding rainfall totals associated with them
for radius in radius_list:

    for year in range(year_s, year_f):

        print(f"Year: {year} - Curv radius: {radius}")

        curv = mv.read(f"{dir_in_curv}/z500_curv{radius}_{year}.grib")

        date_s = datetime(year, 1, 1)
        date_f = datetime(year, 12, 31)
        the_date = date_s
        while the_date <= date_f:

            print(f" - Processing {the_date.strftime("%Y%m%d")}")
            # Determining the maximum curv value in a day 
            the_date_str = the_date.strftime("%Y%m%d")
            dates = np.array(mv.grib_get_string(curv, "dataDate"))
            the_date_index = np.where(dates == the_date_str)[0]
            curv_date = mv.values(curv[the_date_index])
            max_curv_date = np.max(curv_date, axis = 0).astype(np.float32)
            index = np.argmax(curv_date, axis = 0)

            # Reading the daily rainfall value
            tp = mv.read(f"{ERA5_ECPOINT_TP_24H_DIR}/{the_date.strftime("%Y%m")}/Pt_BC_PERC_{the_date.strftime("%Y%m%d")}_024.grib1")
            tp = mv.values(tp).astype(np.float32)

            # Saving the data for curv and rainfall
            dir_out_temp = f"{dir_out}/{radius}/{the_date.strftime("%Y")}/{the_date.strftime("%Y%m%d")}"
            os.makedirs(dir_out_temp, exist_ok=True)
            np.save(f"{dir_out_temp}/max_curv", max_curv_date)
            np.save(f"{dir_out_temp}/tp", tp)

            the_date = the_date + timedelta(days = 1)