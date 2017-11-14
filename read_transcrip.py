#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 16:07:47 2017

@author: Tomas Arias -- Universidad de Antioquia -- GITA
"""

import numpy as np
import os

def decode_transcription():
    #GET PATH OF THE SCRIPT BEING RUN
    path_asr = os.path.dirname(os.path.abspath(__file__))
    
    #Phone index
    path_phoneidx = path_asr+'/data/lang/words.txt'
    ph = []
    phone_idx = open(path_phoneidx, 'r') 
    for line in phone_idx: 
        ph.append(line)
    
    ph = ph[3:-3]
    
    phone = []
    phone_id = np.zeros(len(ph),dtype=int)
    pidx = 0
    for idxp in ph:
        temp_split = idxp.split()
        #Phones 
        phone.append(temp_split[0])
        #Phones index
        phone_id[pidx] = temp_split[1]
        pidx+=1
        
    phone_idx.close()
    #########################################################
    #Transcription
    #########################################################
    fname = path_asr+"/exp/tri1/decode/scoring/17.tra"    
    sig_name = []
    sig_tran = []
    f = open(fname, 'r') 
    for line in f: 
        temp_split = line.split()
        #Speech recording file name
        sig_name.append(temp_split[0])
        sig_tran.append(temp_split[1:])
    
    f.close()

    #Decode the transciptions
    f = open('Transcriptions_result.txt', 'w') #Save transcription
    for tr in range(0,len(sig_name)):
        tr_enc = sig_tran[tr]
        f.write(sig_name[tr]+' ')
        for ph in tr_enc:
            find_phone = np.where(phone_id==int(ph))[0][0]
            f.write(phone[find_phone]+' ')
        f.write('\n')
    f.close()

       
        
        
        