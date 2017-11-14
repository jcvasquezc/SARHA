#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 08:20:40 2017

@author: Tomas Arias -- Universidad de Antioquia -- GITA
"""

import subprocess
import os

#GET PATH OF THE SCRIPT BEING RUN
path_asr = os.path.dirname(os.path.abspath(__file__))

"""
RUN THE ASR
"""
subprocess.call([path_asr+'/run_test_file.sh'])
