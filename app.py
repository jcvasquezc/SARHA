
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 15:00:38 2017

@author: J. C. Vasquez-Correa -- Universidad de Antioquia -- GITA
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import os
from playsound import playsound


import plotly.graph_objs as go
import pandas as pd
import numpy as np
from scipy.io.wavfile import read

import wave, struct

from functools import reduce
import base64

import os,sys,subprocess # We need sys so that we can pass argv to QApplication
import numpy as np
import test_dict,read_transcrip


from utils import get_fs_model, speaker_path, start_recording, stop_recording, trans_bt, playSound

import pygame
path_asr = os.path.dirname(os.path.abspath(__file__))

fs=get_fs_model(path_asr)

stop_process=False
flag_recording=False
app = dash.Dash(__name__)
server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})



styles = {
    'column': {
        'display': 'inline-block',
        'width': '90%',
        'padding': 10,
        'boxSizing': 'boder-box',
        'minHeight': '350px',
        'columnCount': 4,
    },

    'speakID': {
    #'display': 'inline-block',
    'width': '65%',
    'padding': ['0%'  '0%' '0%' '25%'],
    'boxSizing': 'boder-box',
    'columnCount': 3,
    "font-size":"100%",
    "align": 'right',

},

    'pre': {"font-size":"200%", 'width': '50%', 'padding': ['0%'  '0%' '0%' '20%']},

    'pre2': {"font-size":"200%", 'width': '50%', 'padding': ['0%'  '0%' '0%' '30%']},

    'texts': {"font-size":"100%", 'width': '50%', 'padding': ['0%'  '0%' '0%' '41%'], 'display': 'inline-block'},

    'button_record':{},
    'plot': {'width': '70%', 'height': '10%','padding': ['0%'  '0%' '0%' '15%']}


}



token='pk.eyJ1IjoiamN2YXNxdWV6YyIsImEiOiJjajhpOHJzYzEwd2lhMndteGE3dXdoZ2JwIn0.FXt2St8t89mIZ-L-UpCYkg'

image_filename1="./udea.png"
image_filename2="./logoGITA.png"
image_filename3="./logoSARHA.png"
image_button1="./micon.png"
image_button2="./micoff.png"

image_button4="./play.png"
image_button3="./stop.png"



encoded_image1=base64.b64encode(open(image_filename1, 'rb').read())
encoded_image2=base64.b64encode(open(image_filename2, 'rb').read())
encoded_image5=base64.b64encode(open(image_filename3, 'rb').read())

encoded_image3=base64.b64encode(open(image_button1, 'rb').read())
encoded_image4=base64.b64encode(open(image_button2, 'rb').read())

encoded_image6=base64.b64encode(open(image_button3, 'rb').read())
encoded_image7=base64.b64encode(open(image_button4, 'rb').read())



button_test='data:image/png;base64,{}'.format(encoded_image4.decode())

pygame.init()


app.layout = html.Div([

        html.Div([
        #html.H1(children='ANMOTO'),
        html.Title("SARHA"),
        html.Img(src='data:image/png;base64,{}'.format(encoded_image5.decode()), style={'height':'10%', 'width': '20%', 'display': 'inline-block', 'padding': ['0%'  '0%' '0%' '20%']}),
        html.Img(src='data:image/png;base64,{}'.format(encoded_image1.decode()), style={'height':'1%', 'width': '6%', 'display': 'inline-block', 'padding': ['0%'  '0%' '0%' '26%']}),
        html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()), style={'height':"9%", 'width': '8%', 'display': 'inline-block', 'padding': ['0%'  '0%' '0%' '0%']}),
        ]),
        html.Div(["Sistema automático de reconocimiento de habla"], style={"font-size":"200%", 'width': '80%','padding': ['0%'  '0%' '0%' '24%']}),


        html.Div([
            html.Div(["ID hablante"]),
            dcc.Input(
                    placeholder='ID hablante',
                    type='text',
                    value='',
                    id='spkname'
                ),
                        #html.Div(["Gender"]),
            dcc.RadioItems(
                options=[
                    {'label': 'Hombre', 'value': 'male'},
                    {'label': 'Mujer', 'value': 'female'},
                ],
            )
        ], style=styles["speakID"]),

        html.Div([
        html.Div([html.Img(src='data:image/png;base64,{}'.format(encoded_image4.decode()),
        id='button_image', style={'width':'70%'}),
        ], style={ 'display': 'inline-block', 'padding': ['0%'  '0%' '0%' '40%']},
         id='button_rec', n_clicks=0),
        html.Div([html.Img(src='data:image/png;base64,{}'.format(encoded_image6.decode()),
        id='button_image2', style={'width':'50%'}),
        ], style={'display': 'inline-block', 'padding': ['0%'  '0%' '0%' '10%']},
         id='button_play', n_clicks=0)]),



         html.Div([dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Scatter(
                            x=[], y=[], mode = 'lines',
                        ),
                    ],
                    layout=go.Layout(
                        title='Voz',
                            xaxis= dict(
                                        title= 'Tiempo (s)',
                                        ticklen= 5,
                                        zeroline= False,
                                        gridwidth= 2,
                                    ),
                    ),
                ),
                id='plot_speech',
                style=styles['plot'],
            )
         ]),

         html.Div([
            html.Button('Transcribir', id='bt_transcribe'),
            html.Div(id='transcription', children="")
         ], style=styles["pre"]),




    ])





@app.callback(
    dash.dependencies.Output('plot_speech', 'figure'),
    [dash.dependencies.Input('button_rec', 'n_clicks'),
    dash.dependencies.Input('spkname', 'value')])
def update_plot(n_clicks, spkname):
    global path_asr, layoutplot, fs, stop_process
    if stop_process:
        fname=speaker_path(spkname, path_asr)+".wav"
        if os.path.exists(fname):
            fs2, signal=read(fname)
            print(signal)
            signal=signal-np.mean(signal)
            signal=signal/max(abs(signal))
            xd=np.arange(len(signal))/fs2
            print(signal)
        else:
            signal=[]
            xd=[]


    else:
        signal=[]
        xd=[]
    print(signal)
    return go.Figure(data=[go.Scatter(x=xd, y=signal, mode = 'lines')],
                     layout=go.Layout(title='Voz',xaxis= dict(
                                                            title= 'Tiempo (s)',
                                                            ticklen= 5,
                                                            zeroline= False,
                                                            gridwidth= 2)))




@app.callback(
    dash.dependencies.Output('button_image2', 'src'),
    [dash.dependencies.Input('button_play', 'n_clicks'),
    dash.dependencies.Input('spkname', 'value')])
def update_output_play(n_clicks, spkname):
    global path_asr

    if int(n_clicks)>0:
        fname=speaker_path(spkname, path_asr)+".wav"
        print(fname)
        print(os.path.exists(fname))
        if os.path.exists(fname):

            playSound(fname)
    return 'data:image/png;base64,{}'.format(encoded_image7.decode())







@app.callback(
    dash.dependencies.Output('button_image', 'src'),
    [dash.dependencies.Input('button_rec', 'n_clicks'),
    dash.dependencies.Input('spkname', 'value')])
def update_output(n_clicks, spkname):
    global path_asr, fs, stop_process, flag_recording, process


    print(int(n_clicks))
    if int(n_clicks) % 2==0 and int(n_clicks)>1:
        if flag_recording:
            stdout, stderr=stop_recording(process)
            stop_process=True
            print("##################################################")
            print("Terminando procesoooo")
            flag_recording=False
        return 'data:image/png;base64,{}'.format(encoded_image4.decode())
    elif int(n_clicks)>0 and int(n_clicks) % 2!=0 :
        fname=speaker_path(spkname, path_asr)
        process=start_recording(fs,path_asr,fname )
        stop_process=False
        flag_recording=True
        print(fname, process)
        return 'data:image/png;base64,{}'.format(encoded_image3.decode())
    else:
        return 'data:image/png;base64,{}'.format(encoded_image4.decode())

@app.callback(
    dash.dependencies.Output('transcription', 'children'),
    [dash.dependencies.Input('bt_transcribe', 'n_clicks'),
    dash.dependencies.Input('spkname', 'value')])
def update_output(n_clicks, spkname):
    global path_asr
    if n_clicks>0:
        path_audios_test = path_asr+'/frases_es_audio/test/'+spkname+'/'
        tr=trans_bt('m', path_asr, path_audios_test)
        return tr
    else:
        return ''







if __name__ == '__main__':
    app.run_server(debug=True)
