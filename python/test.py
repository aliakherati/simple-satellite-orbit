import numpy as np
import matplotlib.pyplot as plt
import argparse
import satellite as sat
import pandas as pd

# inputs
a = 6378.1370 # minor axis 
b = 6356.7523 # major axis
T = [90, 100, 120, 70, 80, 60] # periods
nsatellite = len(T)

test = sat.Satellite(
    minor_axis = a,
    major_axis = b,
    period = T,
    nsatellite=len(T),
)

