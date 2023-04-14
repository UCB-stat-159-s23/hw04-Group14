import numpy as np
import json
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from ligotools import readligo as rl
from ligotools.utils import *

file_L1 = "data/L-L1_LOSC_4_V2-1126259446-32.hdf5"
file_H1 = "data/H-H1_LOSC_4_V2-1126259446-32.hdf5"

strain_H1, time_H1, chan_dict_H1 = rl.loaddata(file_L1, 'H1')
strain_L1, time_L1, chan_dict_L1 = rl.loaddata(file_H1, 'L1')

def test_loaddata():
    assert type(strain_L1)==np.ndarray and type(time_L1)==np.ndarray and type(chan_dict_L1)==dict
    assert type(strain_H1)==np.ndarray and type(time_H1)==np.ndarray and type(chan_dict_H1)==dict
    

def test_l1_empty():
    assert strain_L1.any()
    assert time_L1.any()
    assert chan_dict_L1 is not None
    
    
def test_h1_empty():
    assert strain_H1.any()
    assert time_H1.any()
    assert chan_dict_H1 is not None

    
def test_dq_channel_to_seglist():
    seg_L1 = readligo.dq_channel_to_seglist(chan_dict_L1)
    seg_H1 = readligo.dq_channel_to_seglist(chan_dict_H1)
    assert type(seg_L1)==list
    assert type(seg_H1)==list
    

    
