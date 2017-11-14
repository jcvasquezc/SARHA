#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 13:37:46 2017

@author: Tomas Arias -- Universidad de Antioquia -- GITA
"""

import os
global path_asr
global path_test
global list_ids

#GET PATH OF THE SCRIPT BEING RUN
path_asr = os.path.dirname(os.path.abspath(__file__))

path_test = path_asr+'/frases_es_audio/test/'
list_ids = os.listdir(path_test)
list_ids.sort()

def make_spkgender(spkgender, path_audios_test):
    '''
    Make spk2gender file
    <speaker_id><gender(m or f)>
    '''
    fname = "spk2gender"
    f = open(path_asr+'/data/test/'+fname, "w")
    print(spkgender)
    idxspk=path_audios_test.split('/')[-2]
    f.write(idxspk+' '+spkgender)
    f.write('\n')

    f.close()

# def make_wav():
#     '''
#     Make wav.scp file
#     <wavfile_id><path_containing_thewavfile>
#     '''
#     fname = "wav.scp"
#     f = open(path_asr+'/data/test/'+fname, "w")
#
#     for idxtest in list_ids:
#         path_audios_test = path_test+idxtest+'/'
#         list_audios_test = os.listdir(path_audios_test)
#         list_audios_test.sort()
#         for idxaudios in list_audios_test:
#                 f.write(idxaudios[0:-4]+' '+path_audios_test+idxaudios)
#                 f.write('\n')
#
#     f.close()


def make_wav(path_audios_test):
    '''
    Make wav.scp file
    <wavfile_id><path_containing_thewavfile>
    '''
    fname = "wav.scp"
    f = open(path_asr+'/data/test/'+fname, "w")

    list_audios_test = os.listdir(path_audios_test)
    list_audios_test.sort()
    for idxaudios in list_audios_test:
        f.write(idxaudios[0:-4]+' '+path_audios_test+idxaudios)
        f.write('\n')

    f.close()



# def make_text_free():
#     '''
#     Make text file when the transcription is unknown
#     <wavfile_id><transcription_of_the_wavfile>
#     '''
#     fname = "text"
#     f = open(path_asr+'/data/test/'+fname, "w")
#     for idxtest in list_ids:
#         path_audios_test = path_test+idxtest+'/'
#         list_audios_test = os.listdir(path_audios_test)
#         list_audios_test.sort()
#         for idxaudios in list_audios_test:
#             f.write(idxaudios[0:-4]+' '+'Mi casa tiene tres cuartos')
#             f.write('\n')
#     f.close()



def make_text_free(path_audios_test):
    '''
    Make text file when the transcription is unknown
    <wavfile_id><transcription_of_the_wavfile>
    '''
    fname = "text"
    f = open(path_asr+'/data/test/'+fname, "w")
    list_audios_test = os.listdir(path_audios_test)
    list_audios_test.sort()
    for idxaudios in list_audios_test:
        f.write(idxaudios[0:-4]+' '+'Mi casa tiene tres cuartos')
        f.write('\n')
    f.close()


# def make_utt2spk():
#     '''
#     Crear utt2spk
#     <wavfile_id><speaker_id>
#     '''
#     fname = "utt2spk"
#     f = open(path_asr+'/data/test/'+fname, "w")
#
#     for idxspk in list_ids:
#         path_audios_test = path_test+idxspk+'/'
#         list_audios_test = os.listdir(path_audios_test)
#         list_audios_test.sort()
#         for idxaudios in list_audios_test:
#                 f.write(idxaudios[0:-4]+' '+idxspk)
#                 f.write('\n')
#     f.close()



def make_utt2spk(path_audios_test):
    '''
    Crear utt2spk
    <wavfile_id><speaker_id>
    '''
    fname = "utt2spk"
    f = open(path_asr+'/data/test/'+fname, "w")

    list_audios_test = os.listdir(path_audios_test)
    list_audios_test.sort()
    idxspk=path_audios_test.split('/')[-2]
    print(idxspk)
    for idxaudios in list_audios_test:
        f.write(idxaudios[0:-4]+' '+idxspk)
        f.write('\n')
    f.close()
