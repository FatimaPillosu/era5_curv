import os

# Define the absolute path to the project's root directory or local git repository
ROOT_DIR = "/perm/mofp/era5_curv"

# Define other main paths relative to the root directory
SCRIPTS_RAW_DIR = os.path.join(ROOT_DIR, 'scripts/raw')
SCRIPTS_PROCESSED_DIR = os.path.join(ROOT_DIR, 'scripts/processed')
DATA_RAW_DIR = os.path.join(ROOT_DIR, 'data/raw')
DATA_COMPUTE_DIR = os.path.join(ROOT_DIR, 'data/compute')
DATA_PLOTS_DIR = os.path.join(ROOT_DIR, 'data/plots')

# Define the absolute path of the directory containing ERA5-related data
ERA5_ECPOINT_CLIMATE_TP_24H_DIR = "/ec/vol/ecpoint/mofp/climate_reference/data/era5_ecpoint/tp_24h_1991_2020"
ERA5_ECPOINT_TP_24H_DIR = "/ec/vol/ecpoint/mofp/reanalysis/ecpoint/SemiOper/ECMWF_ERA5/0001/Rainfall/024/Code2.0.0_Cal1.0.0/Pt_BC_PERC"