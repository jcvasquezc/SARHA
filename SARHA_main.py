# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 15:00:38 2017

@author: Tomas Arias -- Universidad de Antioquia -- GITA
"""
from PyQt5 import QtWidgets,QtGui,QtCore
import ASR_ui #GUI designed using QT Creator
import os,sys,subprocess # We need sys so that we can pass argv to QApplication
import numpy as np
import test_dict,read_transcrip

class ASR_Kaldi(QtWidgets.QMainWindow,ASR_ui.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        ASR_ui.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        #Speech recording button        
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("ASR_UI/micoff.png"))
        self.rec_speech.setIcon(self.icon)
        self.rec_speech.setIconSize(QtCore.QSize(64, 64))
        self.rec_speech.clicked.connect(self.record_speech_bt)
        
        #Female radio button
#        self.radiobt_female.setChecked(True)
        self.radiobt_female.toggled.connect(lambda:self.gender_switch(self.radiobt_female))
        #Male radio button
        self.radiobt_male.toggled.connect(lambda:self.gender_switch(self.radiobt_male))
   
        #Transcription button
        self.transcript_bt.clicked.connect(self.trans_bt)
    
    #ON CLICKED RECORD BUTTON
    def record_speech_bt(self):
        global rec_bt           
        rec_bt = not(rec_bt)
        if (rec_bt):
#            self.rec_speech.setText('Stop')
            self.icon.addPixmap(QtGui.QPixmap("ASR_UI/micon.png"))
            self.rec_speech.setIcon(self.icon)
            #Create folders
            speaker_path(self.speaker_id.displayText())
            #Start recording
            start_recording()
        else:
#            self.rec_speech.setText('Record')
            self.icon.addPixmap(QtGui.QPixmap("ASR_UI/micoff.png"))
            self.rec_speech.setIcon(self.icon)
            stop_recording()
            
    #ON GENDER SELECTION
    def gender_switch(self,gen_sel):
        global spkg
        if gen_sel.isChecked()==True:
            #Set gender
            if gen_sel.text() == 'female':
                spkg = 'f'
            else:
                spkg = 'm'
            
    #ON CLICKED TRANSCRIPTION BUTTON
    def trans_bt(self):
        global spkg,path_asr
        #Make spk2gender file
        test_dict.make_spkgender(spkg)
        #Make wav.scp file (wavfile path)
        test_dict.make_wav()
        #Make text file (transcription)
        test_dict.make_text_free()
        #Make utt2spk (wavfile speaker id)
        test_dict.make_utt2spk()
        #RUN THE ASR
        subprocess.call([path_asr+'/run_test_file.sh'])
        #Decode transcription
        read_transcrip.decode_transcription()
        #Display transcription in the GUI
        tr = display_transcript()
        self.label_transcript.setText(''.join(tr))
        
#Get sampling frequency from model
def get_fs_model(path_audio):
    global fs
    fname = "fs"    
    f = open(path_audio+'/frases_es_audio/'+fname, "r")
    for line in f:
        fs = line
    f.close()     

#Create speaker data
def speaker_path(speakerID):    
    global fname,spkg
    #Create folder for speaker (if necessary)
    path_audio = path_asr+'/frases_es_audio/test/'+speakerID
    if os.path.isdir(path_audio)==False:#Is it already create?
            os.makedirs(path_audio)#If not, create speaker folder
    Nfiles = os.listdir(path_audio+'/')#Get number of files
#    fname = path_audio+'/'+speakerID+'_'+str(len(Nfiles)+1)
    fname = path_audio+'/'+speakerID+'_freetest'
    
#Speech recording using arecord (LINUX)
def start_recording():
    global fs,path_asr,fname  
    #Start recording
    subprocess.Popen(['arecord','-c','1','-t','wav','-f','S16_LE','-r',fs,fname+'.wav'], stdout=subprocess.PIPE)
    
def stop_recording():
    subprocess.Popen(['killall','-KILL','arecord'], stdout=subprocess.PIPE)

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

#MAIN 
if __name__ == "__main__":
    global rec_bt,rec_flag,path_asr  
    #GET PATH OF THE SCRIPT BEING RUN
    path_asr = os.path.dirname(os.path.abspath(__file__))
    #Get fundamental frequency
    get_fs_model(path_asr)
    rec_bt = False
    rec_flag = False
    app = QtWidgets.QApplication(sys.argv)
    asr_win = ASR_Kaldi()
    asr_win.show()
    sys.exit(app.exec_()) 