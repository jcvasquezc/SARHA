#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 13:33:46 2017

@author: Tomas Arias -- Universidad de Antioquia -- GITA
"""

import subprocess
import numpy as np
import os
import test_dict

#GET PATH OF THE SCRIPT BEING RUN
path_asr = os.path.dirname(os.path.abspath(__file__))


#path_test = path_asr+'/frases_es_audio/test/'

"""
#################################################
##########   Make test files   ##################
#################################################
"""
##Make wav.scp file
#test_dict.make_wav()
##Make text
#test_dict.make_text()
##Make utt2spk
#test_dict.make_utt2spk()


"""
#################################################
##############  RUN THE ASR  ####################
#################################################
"""
#subprocess.call([path_asr+'/run_test_file.sh'])