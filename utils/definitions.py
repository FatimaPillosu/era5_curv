import numpy as np

# Thresholds for curvature diagnostic to define (anti)cyclonic features
thr_curv_4_ac_features_vals = [-np.inf, -15, -11, -7, -3, 3, 7, 11, 15, np.inf]
thr_curv_4_ac_features_categories = ["anticyclone", "strong anticyclonic curv", "anticyclonic curv", "weak anticyclonic curv", "straight flow or col", "weak cyclonic curv", "cyclonic curv", "strong cyclonic curv", "cyclone"]