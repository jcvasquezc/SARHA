#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 11:15:27 2017

@author: Tomas Arias -- Universidad de Antioquia -- GITA
"""

import os,sys
from scipy.io.wavfile import read
from scipy.stats import pearsonr
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import numpy as np



#GET PATH OF THE SCRIPT BEING RUN
path_file = os.path.dirname(os.path.abspath(__file__))


path_test = path_file+'/frases_es_audio/test/'
list_ids = os.listdir(path_test)
list_ids.sort()
path_train = path_file+'/frases_es_audio/train/'
list_ids_train = os.listdir(path_train)
list_ids_train.sort()

#Crear wav file como un txt
fname = "wav.scp"    
f = open(fname, "w")

for idxtest in list_ids:
    path_audios_test = path_test+idxtest+'/'
    list_audios_test = os.listdir(path_audios_test)
    list_audios_test.sort()
    for idxaudios in list_audios_test:
            f.write(idxaudios[0:-4]+' '+path_audios_test+idxaudios)
            f.write('\n')
    
#for idxtrain in list_ids_train:
#    path_audios_train = path_train+idxtrain+'/'
#    list_audios_train = os.listdir(path_audios_train)
#    list_audios_train.sort()
#    for idxaudios in list_audios_train:
#            f.write(idxaudios[0:-4]+' '+path_audios_train+idxaudios)
#            f.write('\n')
#    
f.close()    


##Crear text file como un txt.
#fname = "text"    
#f = open(fname, "w")
#
##for idxtest in list_ids:
##    path_audios_test = path_test+idxtest+'/'
##    list_audios_test = os.listdir(path_audios_test)
##    list_audios_test.sort()
##    for idxaudios in list_audios_test:
##            idxtemp = idxaudios[10:-4].find('-')
##            if idxtemp==-1:
##                f.write(idxaudios[0:-4]+' '+idxaudios[10:-4])
##            else:
##                f.write(idxaudios[0:-4]+' '+idxaudios[11:-4])
##            f.write('\n')
##    
#for idxtrain in list_ids_train:
#    path_audios_train = path_train+idxtrain+'/'
#    list_audios_train = os.listdir(path_audios_train)
#    list_audios_train.sort()
#    for idxaudios in list_audios_train:
#            idxtemp = idxaudios[10:-4].find('-')
#            if idxtemp==-1:
#                f.write(idxaudios[0:-4]+' '+idxaudios[10:-4])
#            else:
#                f.write(idxaudios[0:-4]+' '+idxaudios[11:-4])
#            f.write('\n')
#    
#f.close()    
#
##Crear utt2spk file como un txt.
#fname = "utt2spk"    
#f = open(fname, "w")
##
##for idxtest in list_ids:
##    path_audios_test = path_test+idxtest+'/'
##    list_audios_test = os.listdir(path_audios_test)
##    list_audios_test.sort()
##    for idxaudios in list_audios_test:
##            f.write(idxaudios[0:-4]+' '+idxaudios[0:5])
##            f.write('\n')
###    
#for idxtrain in list_ids_train:
#    path_audios_train = path_train+idxtrain+'/'
#    list_audios_train = os.listdir(path_audios_train)
#    list_audios_train.sort()
#    for idxaudios in list_audios_train:
#            f.write(idxaudios[0:-4]+' '+idxaudios[0:5])
#            f.write('\n')
#    
#f.close() 