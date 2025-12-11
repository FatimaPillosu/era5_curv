#!/bin/bash

#######################################################
# CODE DESCRIPTION
# retrieve_era5_z500.sh retrieves from MARS 500 hPa geopotential 
# height every 6 hours at the spatial resolution of 0.5 degrees. 
# Runtime: the code retrieves one year of data, on average, in half 
# day, but the retrieval speed can vary significantly due to MARS 
# traffic.

# INPUT PARAMETERS DESCRIPTION
# year_s (integer, in YYYY format): start year to retrieve.
# year_f (integer, in YYYY format): final year to retrieve.
# git_repo (string): repository's local path.
# dir_out (string): relative path containing the retrieved era5 z500.

# INPUT PARAMETERS
year_s=1940
year_f=2024
git_repo="/perm/mofp/era5_curv"
dir_out="data/raw/era5/z500"
#######################################################


# Create the database where to store era5's z500
dir_db_temp="${git_repo}/${dir_out}"
mkdir -p ${dir_db_temp}
main_subdir=$(echo "$dir_out" | sed -n 's|.*raw/\([^/]*\).*|\1|p')
chmod -R 775 ${git_repo}/data/raw/${main_subdir} # assign appropriate permission for collaborators

# Retrieve and store era5's z500
for year in $(seq ${year_s} ${year_f}); do

      for month in 01 02 03 04 05 06 07 08 09 10 11 12 ; do # separate the retrievals per month to improve database access efficiency

            last_day=$(date -d "$year-$month-01 +1 month -1 day" +"%d")

mars <<EOF 
      retrieve,
            class=ea,
            date=${year}${month}01/to/${year}${month}${last_day},
            expver=1,
            levelist=500,
            levtype=pl,
            param=129.128,
            step=0/6,
            stream=oper,
            time=06:00:00/18:00:00,
            type=fc,
            grid=0.5/0.5,
            target="${dir_db_temp}/z500_${year}_${month}.grib"
EOF

      done

      # Merge the monthly files to create a single file per year
      grib_copy ${dir_db_temp}/z500_${year}_*.grib ${dir_db_temp}/z500_${year}.grib
      rm -rf ${dir_db_temp}/z500_${year}_*.grib
      chmod 775 ${dir_db_temp}/z500_${year}.grib # assign appropriate permission for collaborators

done