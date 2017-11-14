# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 15:00:38 2017

@author: Tomas Arias -- Universidad de Antioquia -- GITA
Modifide by J. C. Vásquez-Correa -- Universidad de Antioquia -- GITA
"""

import os, sys, subprocess, wave, struct, signal
import test_dict,read_transcrip
import pygame

def get_fs_model(path_audio):
    global fs
    fname = "fs"
    f = open(path_audio+'/frases_es_audio/'+fname, "r")
    for line in f:
        fs = line
    f.close()
    return fs

#Create speaker data
def speaker_path(speakerID, path_asr):
    #Create folder for speaker (if necessary)
    path_audio = path_asr+'/frases_es_audio/test/'+speakerID
    if os.path.isdir(path_audio)==False:#Is it already create?
            os.makedirs(path_audio)#If not, create speaker folder
    Nfiles = os.listdir(path_audio+'/')#Get number of files
    fname = path_audio+'/'+speakerID+'_freetest'
    return fname


#Speech recording using arecord (LINUX)
def start_recording(fs,path_asr,fname  ):
    #Start recording
    process=subprocess.Popen(['arecord','-c','1','-t','wav','-f','S16_LE','-r',fs,fname+'.wav'], stdout=subprocess.PIPE)
    return process

def stop_recording(process):
    process.send_signal(signal.SIGINT)
    stdout, stderr=process.communicate()
    return stdout, stderr


def display_transcript():
    spk_id = []
    spk_tr = [] #transcription
    f = open('Transcriptions_result.txt', 'r')
    for line in f:
        temp_split = line.split()
        #Speech recording file name
#        spk_id.append(temp_split[0])
        temp_tr = temp_split[1:]
        for tr in temp_tr:
            spk_tr.extend([tr+' '])
        spk_id.append(spk_tr)
    return spk_id[0]

def playSound(filename):
    
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()


def trans_bt(spkg,  path_asr, path_audios_test):
    #Make spk2gender file
    test_dict.make_spkgender(spkg, path_audios_test)
    #Make wav.scp file (wavfile path)
    test_dict.make_wav(path_audios_test)
    #Make text file (transcription)
    test_dict.make_text_free(path_audios_test)
    #Make utt2spk (wavfile speaker id)
    test_dict.make_utt2spk(path_audios_test)
    #RUN THE ASR
    subprocess.call([path_asr+'/run_test_file.sh'])
    #Decode transcription
    read_transcrip.decode_transcription()
    #Display transcription in the GUI
    tr = display_transcript()
    return tr
