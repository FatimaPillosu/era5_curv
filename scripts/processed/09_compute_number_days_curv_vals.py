import sys
utils_dir = '/perm/mofp/era5_curv'
if utils_dir not in sys.path:
    sys.path.append(utils_dir)
import os
import numpy as np
import metview as mv
from utils.paths import DATA_RAW_DIR, DATA_COMPUTE_DIR
from utils.definitions import thr_curv_4_ac_features_vals

np.set_printoptions(threshold=sys.maxsize) # to print full numpy arrays (useful for debugging)


############################################################################
# DESCRIPTION CODE
# 09_compute_number_days_curv_vals.py computes the number of days, per year, in which 
# curv exceeds certain values.
#Runtime: ~ 18 hours.

# DESCRIPTION INPUT PARAMETERS
# year_s (integer, format YYYY): start year to consider.
# year_f (integer, format YYYY): final year to consider.
# radius_list (list of integers, adimensional): list of radius used to compute the curv diagnostic.
# dir_in (string): relative path of the directory containing the average curv diagnostic.
# dir_out (string): relative path of the directory containing the trend plots.

# INPUT PARAMETERS
year_s = 1940
year_f = 2024
radius_list = [500, 1000, 2000, 3000]
dir_in = os.path.join(DATA_RAW_DIR, "era5/curv")
dir_out = os.path.join(DATA_COMPUTE_DIR, "09_number_days_curv_vals")
############################################################################


# Plotting the average CURV, against climatology, for a specific season
for radius in radius_list:

    # Computing the number of days in which curv exceeds a certain value
    for year in range(year_s, year_f + 1):

        print(f"Year: {year} - Curv radius: {radius}")

        # Reading the curv variable
        curv = mv.read(f"{dir_in}/z500_curv{radius}_{year}.grib")
        
        # Computing the number of days per season
        date_list = np.array(mv.grib_get_string(curv, "date"), dtype='datetime64[D]')

        # DJF
        dates_mask = np.array((date_list >= np.datetime64(f'{year}1201')) & (date_list <= np.datetime64(f'{year}1231')) | (date_list >= np.datetime64(f'{year}0101')) & (date_list < np.datetime64(f'{year}0301')))
        dates_mask = np.where(dates_mask)[0]
        curv_DJF = curv[dates_mask]
        
        dates_mask = np.array((date_list >= np.datetime64(f'{year}0301')) & (date_list <= np.datetime64(f'{year}0531'))) # MAM
        dates_mask = np.where(dates_mask)[0]
        curv_MAM = curv[dates_mask]
        
        dates_mask = np.array((date_list >= np.datetime64(f'{year}0601')) & (date_list <= np.datetime64(f'{year}0831'))) # JJA
        dates_mask = np.where(dates_mask)[0]
        curv_JJA = curv[dates_mask]
        
        dates_mask = np.array((date_list >= np.datetime64(f'{year}0901')) & (date_list <= np.datetime64(f'{year}1130'))) # SON
        dates_mask = np.where(dates_mask)[0]
        curv_SON = curv[dates_mask]

        dir_out_temp = f"{dir_out}/{radius}/{year}" # creating the uotput directory
        os.makedirs(dir_out_temp, exist_ok=True)

        for ind_thr_curv in range(len(thr_curv_4_ac_features_vals) - 1):
            
            thr_curv_low = thr_curv_4_ac_features_vals[ind_thr_curv]
            thr_curv_up = thr_curv_4_ac_features_vals[ind_thr_curv + 1]
            print(f"    - thr_curv_low = {thr_curv_low} and thr_curv_up = {thr_curv_up}")
        
            curv_num_days_DJF = mv.sum( (curv_DJF > thr_curv_low) & (curv_DJF < thr_curv_up ) )
            curv_num_days_MAM = mv.sum( (curv_MAM > thr_curv_low) & (curv_MAM < thr_curv_up ) )
            curv_num_days_JJA = mv.sum( (curv_JJA > thr_curv_low) & (curv_JJA < thr_curv_up ) )
            curv_num_days_SON = mv.sum( (curv_SON > thr_curv_low) & (curv_SON < thr_curv_up ) )

            mv.write(f"{dir_out_temp}/av_curv_{year}_DJF_{thr_curv_low}_{thr_curv_up}.grib", curv_num_days_DJF)
            mv.write(f"{dir_out_temp}/av_curv_{year}_MAM_{thr_curv_low}_{thr_curv_up}.grib", curv_num_days_MAM)
            mv.write(f"{dir_out_temp}/av_curv_{year}_JJA_{thr_curv_low}_{thr_curv_up}.grib", curv_num_days_JJA)
            mv.write(f"{dir_out_temp}/av_curv_{year}_SON_{thr_curv_low}_{thr_curv_up}.grib", curv_num_days_SON)