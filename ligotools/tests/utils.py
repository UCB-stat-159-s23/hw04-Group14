from ligotools import utils 
from ligotools import readligo

from scipy.io import wavfile
import numpy as np
import json
import h5py
from scipy.interpolate import interp1d
from scipy.signal import butter, filtfilt, iirdesign, zpk2tf, freqz
import pytest

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

fnjson = 'data/'+"BBH_events_v3.json"

strain_H1, time_H1, chan_dict_H1 = rl.loaddata("data/H-H1_LOSC_4_V2-1126259446-32.hdf5", 'H1')
strain_L1, time_L1, chan_dict_L1 = rl.loaddata("data/L-L1_LOSC_4_V2-1126259446-32.hdf5", 'L1')

NFFT = 4*fs
Pxx_H1, freqs = mlab.psd(strain_H1, Fs = fs, NFFT = NFFT)
Pxx_L1, freqs = mlab.psd(strain_L1, Fs = fs, NFFT = NFFT)
psd_H1 = interp1d(freqs, Pxx_H1)
psd_L1 = interp1d(freqs, Pxx_L1)

time = time_H1 # H1 and L1 share the same time vector
dt =  time[1]-time[0] 


#test whiten function:

def test_whiten():
    subject=readligo.FileList("./audio")
    files=subject.list
    assert eventname+"_H1_whitenbp.wav" in files 
    assert eventname+"_L1_whitenbp.wav" in files

#test reqshift function

def test_reqshift_1():
    fs=4096
    fshift=400
    reqshift_H1 = utils.reqshift(strain_H1_whitenbp, fshift, fs)
    reqshift_L1 = utils.reqshift(strain_L1_whitenbp, fshift, fs)
    assert reqshift_H1 is not None
    assert reqshift_L1 is not None
    
    
#test write wavfiles function

def test_write_wavfile():
    subject = readligo.FileList("./audio")
    files = subject.list
    assert eventname+"_H1_whitenbp.wav" in files 
    assert eventname+"_L1_whitenbp.wav" in files
    

#test plot psd function

def test_plot_psd():
    assert type(etime) is np.ndarray
    assert type(tevent) is float