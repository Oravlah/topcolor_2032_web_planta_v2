
import pymysql
import random
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash import dash_table
import plotly.graph_objects as go
from datetime import datetime as dat
import dash_bootstrap_components as dbc
import json
import requests
from pandas.io.json import json_normalize
from datetime import date
from datetime import timedelta
from server import app
from dotenv import load_dotenv
import os
import calendar
import time
from datetime import datetime

import sqlite3

import dash_daq as daq


# Ruta base del proyecto
BASEDIR = os.path.dirname(os.path.abspath(__file__))
ENV_VARS = os.path.join(BASEDIR, ".env")
# se cargan las variables de entorno
load_dotenv(ENV_VARS)
########################
host = os.environ.get('IP_API')
port = os.environ.get('PORT')
host_ege = os.environ.get('IP_API_EGE')

lineas=[1,2,3,4,5,6,7,8,9,11,12]
nombre_lineas=["7","aditivo",3]


hora=dat.now()

layout = html.Div([
    dcc.Location(id='urlmantener_config', refresh=True),
    dcc.Location(id='url_msj_ok', refresh=True),
                        dbc.Row([dbc.Col([], width=2),
                             dbc.Col([dbc.Row([dbc.Card([
                                 dbc.CardBody([html.H4('Ingresar Mensaje', style={'text-align': 'center'}),

                                          dbc.Row([dbc.Col([ dcc.Input(value='', type='text', id='input_msj',
                                                         style={"width": "100%", 'background-color': 'black',
                                                                'color': 'white', 'text-align': 'center',
                                                                'font-size': '30px', 'font-weight': 'bold',
                                                                'margin-top': '10px'})], width=12)
                                            ]),

                                         dbc.Row([dbc.Col([ dcc.Dropdown(id='menu_lineas', placeholder='Seleccione Linea ', options=[
                                                                                   {'label': 'Linea 1', 'value': '1'},
                                                                                   {'label': 'Linea 2', 'value': '2'},
                                                                                   {'label': 'Linea 3', 'value': '3'},
                                                                                    {'label': 'Linea 4', 'value': '4'},
                                                                                    {'label': 'Linea 5', 'value': '5'},
                                                                                    {'label': 'Linea 6', 'value': '6'},
                                                                                    {'label': 'Linea 7', 'value': '7'},
                                                                                    {'label': 'Linea 8', 'value': '8'},
                                                                               ],
                                                                               value='',
                                                      style={'width': '100%','margin-top':'20px', 'color': 'black'}),
                                                dcc.Interval(id='interval_menu_lineas', interval=2000, n_intervals=0),
                                                                    ], width=6),
                                                dbc.Col([dbc.Button('AJUSTAR MENSAJES', color="info", id='btn_ingresar', n_clicks=0,
                                                         style={'margin-top':'20px'})], width=6)
                                            ]) ,
                                               dbc.Row([
                                            dbc.Col([html.Div(id='result',style={'margin-left':'30px','margin-top':'20px'}),
                                             html.Div(id='mostrar_btn',style={'margin-left':'160px','margin-top':'20px'})])

                                               ]),



                                               ])],
                                 style={"height": "15rem", 'border': 'black 2px solid', 'text-align': 'center',
                                        'margin-left': '5px', 'margin-top': '10px'})
                             ]),

                             ], width=8),


                    ]),

                    dbc.Row([dbc.Col([html.H4('Linea 1', style={'text-align': 'center', 'margin-top': '40px'})], width=4),
                            dbc.Col([html.H4('Linea 2', style={'text-align': 'center', 'margin-top': '40px'})], width=4),
                            dbc.Col([html.H4('Linea 3', style={'text-align': 'center', 'margin-top': '40px'})], width=4),
                    ]),

                    dbc.Row([dbc.Col([dcc.Input(value='', type='text', id='show_msj1', disabled=True,
                                                         style={"width": "100%", 'background-color': 'black',
                                                                'color': 'white', 'text-align': 'center',
                                                                'font-size': '25px', 'font-weight': 'bold',
                                                                'margin-top': '5px'})], width=4),
                            dbc.Col([dcc.Input(value='', type='text', id='show_msj2', disabled=True,
                                                         style={"width": "100%", 'background-color': 'black',
                                                                'color': 'white', 'text-align': 'center',
                                                                'font-size': '25px', 'font-weight': 'bold',
                                                                'margin-top': '5px'})], width=4),
                            dbc.Col([dcc.Input(value='', type='text', id='show_msj3', disabled=True,
                                                         style={"width": "100%", 'background-color': 'black',
                                                                'color': 'white', 'text-align': 'center',
                                                                'font-size': '25px', 'font-weight': 'bold',
                                                                'margin-top': '5px'})], width=4),

                    ]),

                    dbc.Row([dbc.Col([html.H4('Linea 4', style={'text-align': 'center', 'margin-top': '40px'})], width=4),
                            dbc.Col([html.H4('Linea 5', style={'text-align': 'center', 'margin-top': '40px'})], width=4),
                            dbc.Col([html.H4('Linea 6', style={'text-align': 'center', 'margin-top': '40px'})], width=4),
                    ]),

                    dbc.Row([dbc.Col([dcc.Input(value='', type='text', id='show_msj4', disabled=True,
                                                         style={"width": "100%", 'background-color': 'black',
                                                                'color': 'white', 'text-align': 'center',
                                                                'font-size': '25px', 'font-weight': 'bold',
                                                                'margin-top': '5px'})], width=4),
                            dbc.Col([dcc.Input(value='', type='text', id='show_msj5', disabled=True,
                                                         style={"width": "100%", 'background-color': 'black',
                                                                'color': 'white', 'text-align': 'center',
                                                                'font-size': '25px', 'font-weight': 'bold',
                                                                'margin-top': '5px'})], width=4),
                            dbc.Col([dcc.Input(value='', type='text', id='show_msj6', disabled=True,
                                                         style={"width": "100%", 'background-color': 'black',
                                                                'color': 'white', 'text-align': 'center',
                                                                'font-size': '25px', 'font-weight': 'bold',
                                                                'margin-top': '5px'})], width=4),

                    ]),

                    dbc.Row([dbc.Col([html.H4('Linea 7', style={'text-align': 'center', 'margin-top': '40px'})], width=4),
                             dbc.Col([html.H4('Linea 8', style={'text-align': 'center', 'margin-top': '40px'})], width=4),
                             dbc.Col([html.H4('Linea 9', style={'text-align': 'center', 'margin-top': '40px'})], width=4),
                             ]),

                    dbc.Row([dbc.Col([dcc.Input(value='', type='text', id='show_msj7', disabled=True,
                                style={"width": "100%", 'background-color': 'black',
                                       'color': 'white', 'text-align': 'center',
                                       'font-size': '25px', 'font-weight': 'bold',
                                       'margin-top': '5px'})], width=4),
                         dbc.Col([dcc.Input(value='', type='text', id='show_msj8', disabled=True,
                                            style={"width": "100%", 'background-color': 'black',
                                                   'color': 'white', 'text-align': 'center',
                                                   'font-size': '25px', 'font-weight': 'bold',
                                                   'margin-top': '5px'})], width=4),
                         dbc.Col([dcc.Input(value='', type='text', id='show_msj9', disabled=True,
                                            style={"width": "100%", 'background-color': 'black',
                                                   'color': 'white', 'text-align': 'center',
                                                   'font-size': '25px', 'font-weight': 'bold',
                                                   'margin-top': '5px'})], width=4),

                         ]),

                    dbc.Row([dbc.Col([html.H4('Linea 10', style={'text-align': 'center', 'margin-top': '40px'})], width=4),
                         dbc.Col([html.H4('Linea 11', style={'text-align': 'center', 'margin-top': '40px'})], width=4),
                         dbc.Col([html.H4('Linea 12', style={'text-align': 'center', 'margin-top': '40px'})], width=4),
                         ]),

                    dbc.Row([dbc.Col([dcc.Input(value='', type='text', id='show_msj10', disabled=True,
                                            style={"width": "100%", 'background-color': 'black',
                                                   'color': 'white', 'text-align': 'center',
                                                   'font-size': '25px', 'font-weight': 'bold',
                                                   'margin-top': '5px'})], width=4),
                         dbc.Col([dcc.Input(value='', type='text', id='show_msj11', disabled=True,
                                            style={"width": "100%", 'background-color': 'black',
                                                   'color': 'white', 'text-align': 'center',
                                                   'font-size': '25px', 'font-weight': 'bold',
                                                   'margin-top': '5px'})], width=4),
                         dbc.Col([dcc.Input(value='', type='text', id='show_msj12', disabled=True,
                                            style={"width": "100%", 'background-color': 'black',
                                                   'color': 'white', 'text-align': 'center',
                                                   'font-size': '25px', 'font-weight': 'bold',
                                                   'margin-top': '5px'})], width=4),

                         ]),



                            dbc.Row([dbc.Col([], width=4),

                                         ]),
                                            dcc.Interval(id='interval_show_lineas', interval=5000, n_intervals=0),


dbc.Row([dbc.Col([html.Div(id='res1')])]),
])



############################################################################# CALLBACK CON INPUT PARA MODIFICAR MENSAJES 1 2 3
@app.callback(
    [Output('show_msj1', 'value'),
     Output('show_msj2', 'value'),
     Output('show_msj3', 'value'),
],
    [Input('interval_show_lineas', 'n_intervals')])
def update_show_lineas123(value):
    print(f"entro a ultimo dato")
    try:
        msj1= lectura_msj(lineas[0])
        msj2 = lectura_msj(lineas[1])
        msj3 = lectura_msj(lineas[2])


        print('returnxxxxxxxxxxxxxxxxxxx',msj1)
        return (msj1,msj2,msj3)
    except:
        error= '--'
        return (error,error,error)

############################################################################# CALLBACK CON INPUT PARA MODIFICAR MENSAJES 4 5 6
@app.callback(
    [Output('show_msj4', 'value'),
     Output('show_msj5', 'value'),
     Output('show_msj6', 'value'),
],
    [Input('interval_show_lineas', 'n_intervals')])
def update_show_lineas456(value):
    print(f"entro a ultimo dato")
    try:
        msj4= lectura_msj(lineas[3])
        msj5 = lectura_msj(lineas[4])
        msj6 = lectura_msj(lineas[5])

        return (msj4,msj5,msj6)
    except:
        error= '--'
        return (error,error,error)

############################################################################# CALLBACK CON INPUT PARA MODIFICAR MENSAJES 7 8 9
@app.callback(
    [Output('show_msj7', 'value'),
     Output('show_msj8', 'value'),
     Output('show_msj9', 'value'),
],
    [Input('interval_show_lineas', 'n_intervals')])
def update_show_lineas789(value):
    print(f"entro a ultimo dato")
    try:
        msj7= lectura_msj(lineas[6])
        msj8 = lectura_msj(lineas[7])
        #msj9 = lectura_msj(lineas[8])  NO EXISTE LINEA

        return (msj7, msj8, '--')
    except:
        error= '--'
        return (error,error,error)

############################################################################# CALLBACK CON INPUT PARA MODIFICAR MENSAJES 10, 11, 12
@app.callback(
    [Output('show_msj10', 'value'),
     Output('show_msj11', 'value'),
     Output('show_msj12', 'value'),
],
    [Input('interval_show_lineas', 'n_intervals')])
def update_show_lineas10(value):
    print(f"entro a ultimo dato")
    try:
        msj10= lectura_msj(lineas[9])
        msj11 = lectura_msj(lineas[10])
        msj12 = lectura_msj(lineas[11])

        return (msj10, msj11, msj12)
    except:
        error= '--'
        return (error,error,error)

############################## FUNCION LECTURAS MENSAJES
def lectura_msj(linea):

    url = f"http://{host}:{port}/mensaje_panel/&{linea}"
    response = requests.get(url)

    salida_json = response.json()
    json_object = json.loads(salida_json)
    mensaje = json_object['mensaje']


    return mensaje

@app.callback([dash.dependencies.Output('result', 'children'),
               dash.dependencies.Output('res1', 'children'),
                dash.dependencies.Output('input_msj', 'value'),
                dash.dependencies.Output('menu_lineas', 'value'),
],
              [dash.dependencies.Input('btn_ingresar', 'n_clicks')],
              [dash.dependencies.State('input_msj', 'value'),
                dash.dependencies.State('menu_lineas', 'value'),
])
def display_result_ajuste(n_clicks,msj1, menu):
    if n_clicks > 0:
        print('menu',menu)
        if not msj1 or not menu:
            return ( html.Div(html.H3('Debe completar todos los campos', style={'color': 'red'})), '', '','')

        else:
            payload = {
                "msj1": msj1,

            }
            #################### FUNCION QUE ENVIA MODIFICACIN PARA LOS MENSAJES ATRAVEZ DE POST

            #r = requests.post('http://' + host_api + ':' + port + '/mensajes/1', json=payload)
            #print('post 2', r.text)
            #response_dict = json.loads(r.json())
            #print(type(response_dict))
            url = 'http://'+host+':'+port+'/mensaje_panel'
            msje_1 = {'linea': menu, 'mensaje': msj1}



            m1 = requests.post(url, json=msje_1)

            print(m1.text)



        return ('',msj(), '','')

    else:
        return ('', '', '','')


########################################MENSAJE MODAL
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


def msj():
    return html.Div(
    [
        dbc.Button("Open modal", id="open", n_clicks=1,style={'display':'none'}),
        dbc.Modal(
            [
                dbc.ModalHeader("TOP-COLOR"),
                dbc.ModalBody("Mensaje Ingresado correctamente"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="modal",
            is_open=False,
        ),
    ]
)




########################################################### CALLBACK Q REDIRIGEN A HOME O A CONFIGURACION
####################################
@app.callback(Output('url_msj_ok', 'pathname'),
              [Input('volver_msj_ok', 'n_clicks')],)
def registro_volver(n_clicks):
    if n_clicks > 0:
        time.sleep(3)
        return '/configuracion'


@app.callback(Output('urlmantener_config', 'pathname'),
              [Input('mantener_config', 'n_clicks')],)
def registro_error(n_clicks):
    if n_clicks > 0:
        return '/configuracion'
