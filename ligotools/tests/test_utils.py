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

strain_H1, time_H1, chan_dict_H1 = readligo.loaddata("data/H-H1_LOSC_4_V2-1126259446-32.hdf5", 'H1')
strain_L1, time_L1, chan_dict_L1 = readligo.loaddata("data/L-L1_LOSC_4_V2-1126259446-32.hdf5", 'L1')

time = time_H1 
dt =  time[1]-time[0] 
fnjson = "data/BBH_events_v3.json"
events = json.load(open(fnjson,"r"))
eventname = 'GW150914'
event = events[eventname]
fs=event['fs']
tevent = event['tevent']
deltat_sound = 2.
indxd = np.where((time >= tevent-deltat_sound) & (time < tevent+deltat_sound))

NFFT = 4*fs
Pxx_H1, freqs = mlab.psd(strain_H1, Fs = fs, NFFT = NFFT)
Pxx_L1, freqs = mlab.psd(strain_L1, Fs = fs, NFFT = NFFT)
psd_H1 = interp1d(freqs, Pxx_H1)
psd_L1 = interp1d(freqs, Pxx_L1)


#test whiten function:

def test_whiten():
    assert type(strain_H1) == np.ndarray
    assert dt is not None
    
    
#data for reqshift function

data = np.random.normal(1,10000,100)
fshift = 200
fband = event['fband']
NFFT = 4*fs
bb, ab = butter(4, [fband[0]*2./fs, fband[1]*2./fs], btype='band')
normalization = np.sqrt((fband[1]-fband[0])/(fs/2))
Pxx_H1, freqs = mlab.psd(strain_H1, Fs = fs, NFFT = NFFT)
Pxx_L1, freqs = mlab.psd(strain_L1, Fs = fs, NFFT = NFFT)
psd_H1 = interp1d(freqs, Pxx_H1)
psd_L1 = interp1d(freqs, Pxx_L1)
strain_H1_whiten = utils.whiten(strain_H1,psd_H1,dt)
strain_L1_whiten = utils.whiten(strain_L1,psd_L1,dt)
strain_H1_whitenbp = filtfilt(bb, ab, strain_H1_whiten) / normalization
strain_L1_whitenbp = filtfilt(bb, ab, strain_L1_whiten) / normalization
    
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
    assert type(fs) is int
    assert type(utils.write_wavfile(eventname,fs,data)) is not None
    
    
#data for plot psd function
template_offset =16
etime = time+template_offset
tevent = event['tevent']

#test plot psd function

def test_plot_psd():
    assert type(etime) is np.ndarray
    assert type(tevent) is float