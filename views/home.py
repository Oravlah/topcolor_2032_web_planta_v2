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

#nota:
#por programacion, el orden es importante, por lo que solo se puede usar [1,2,3] ,[4,5,6], [7,8,9]
#donde 8 es editivo
#pero para las lineas, la base de datos 3 es para aditivo y 8 para linea 3, por lo que esto se cambia en el nombre lineas=[1,2,8] nombre_lineas=[1,2,3]


# Ruta base del proyecto
BASEDIR = os.path.dirname(os.path.abspath(__file__))
ENV_VARS = os.path.join(BASEDIR, ".env")
# se cargan las variables de entorno
print(BASEDIR)
#os.chdir("..") #bajo un nivel
salida=os.getcwd()  #nuevo path
print(salida)

ENV_VARS = os.path.join(salida, ".env")
load_dotenv(ENV_VARS)

########################
host = os.environ.get('IP_API')
port = os.environ.get('PORT')
host_ege = os.environ.get('IP_API_EGE')
# ##########################################   MENSAJES DEL .ENV
msj1 = os.environ.get('MSJ1')
msj2 = os.environ.get('MSJ2')
msj3 = os.environ.get('MSJ3')
port_web = os.environ.get('PUERTO_WEB')
rango_ini = os.environ.get('RANGO_INI')
rango_fin = os.environ.get('RANGO_FIN')

interval=os.environ.get('interval')
print(f"interval es : {interval}")
print(f"host es : {host}")

interval=int(interval)
n_intervals=os.environ.get('n_intervals')


range= [rango_ini, rango_fin]

if port_web=="8500":
 lineas=[1,2,8]
 nombre_lineas=[1,2,3]

elif port_web=="8501":
 lineas=[4,5,6]
 nombre_lineas=[4,5,6]


else: #pantalla 8502
  lineas=[7,3,8]
  nombre_lineas=["7","aditivo",3]

##################################################
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

hora=dat.now()

layout = html.Div([
                        html.Meta(httpEquiv="refresh", content="300"),  # refresh pagina
                    dbc.Row([
                             dbc.Col([dbc.Row([dbc.Card([
                                                    dbc.CardBody([dbc.Row([ dbc.Col([dcc.Input(value=f'Línea {nombre_lineas[0]}', type='text', id='datox', disabled=True, style={"width": "100%",  'background-color': ' #5dade2 ','color':'white','text-align': 'center','font-size': '25px'})])]),
                                                                  dbc.Row([dbc.Col([html.Div(id='rend_teo1')])]),
                                                                  dbc.Row([dbc.Col([html.H6('EGE',style={'margin-top':'10px'})]),
                                                                            dbc.Col([dcc.Input(value='0000', type='text', id='dato1', disabled=True, style={'margin-top':'5px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '30px'})]),

                                                                           ]),
                                                                  dbc.Row([dbc.Col([html.H6('Disponibilidad',style={'margin-top':'10px'})]),
                                                                            dbc.Col([dcc.Input(value='0000', type='text', id='dato2', disabled=True, style={'margin-top':'5px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '30px'})]),

                                                                        ]),
                                                                    dbc.Row([dbc.Col([html.H6('Desempeño',style={'margin-top':'10px'})]),
                                                                            dbc.Col([dcc.Input(value='0000', type='text', id='dato3', disabled=True, style={'margin-top':'5px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '30px'})]),

                                                                  ]),
                                                                    dbc.Row([dbc.Col([dcc.Input(value='---', type='text', id='t_deten_1', disabled=True, style={'margin-top':'5px',"width": "100%",  'background-color': ' #5dade2 ','color':'white','text-align': 'left','font-size': '25px'})])]),


                                                            ])],style={"height": "21rem",'border': 'black 2px solid','text-align':'left','margin-left':'10px','margin-top':'10px'}
                                                            )]),
################################################################################################################################3
                                        dbc.Row([dbc.Card([
                                                dbc.CardBody([dbc.Row([dbc.Col([dcc.Input(value=f'Línea {nombre_lineas[1]}', type='text', id='datox', disabled=True, style={"width": "100%",  'background-color': ' #5dade2 ','color':'white','text-align': 'center','font-size': '25px'})])]),
                                                              dbc.Row([dbc.Col([html.Div(id='rend_teo2')])]),
                                                                  dbc.Row([dbc.Col([html.H6('EGE',style={'margin-top':'10px'})]),
                                                                            dbc.Col([dcc.Input(value='0000', type='text', id='ege_ad', disabled=True, style={'margin-top':'5px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '30px'})]),

                                                                           ]),
                                                                  dbc.Row([dbc.Col([html.H6('Disponibilidad',style={'margin-top':'10px'})]),
                                                                            dbc.Col([dcc.Input(value='0000', type='text', id='disp_ad', disabled=True, style={'margin-top':'5px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '30px'})]),

                                                                        ]),
                                                                    dbc.Row([dbc.Col([html.H6('Desempeño',style={'margin-top':'10px'})]),
                                                                            dbc.Col([dcc.Input(value='0000', type='text', id='desem_ad', disabled=True, style={'margin-top':'5px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '30px'})]),

                                                                  ]),

                                                                    dbc.Row([dbc.Col([dcc.Input(value='---', type='text', id='t_deten_2', disabled=True, style={'margin-top':'5px',"width": "100%",  'background-color': ' #5dade2 ','color':'white','text-align': 'left','font-size': '25px'})])]),

                                                            ])],style={"height": "21rem",'border': 'black 2px solid','text-align':'left','margin-top':'10px','margin-left':'10px'}
                                                            )]),
##########################################################################################################################
                                 dbc.Row([dbc.Card([
                                                dbc.CardBody([dbc.Row([dbc.Col([dcc.Input(value=f'Línea {nombre_lineas[2]}', type='text', id='datox', disabled=True, style={"width": "100%",  'background-color': ' #5dade2 ','color':'white','text-align': 'center','font-size': '25px'})])]),
                                                              dbc.Row([dbc.Col([html.Div(id='rend_teo3')])]),
                                                                  dbc.Row([dbc.Col([html.H6('EGE',style={'margin-top':'10px'})]),
                                                                            dbc.Col([dcc.Input(value='0000', type='text', id='dato9', disabled=True, style={'margin-top':'5px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '30px'})]),

                                                                           ]),
                                                                  dbc.Row([dbc.Col([html.H6('Disponibilidad',style={'margin-top':'10px'})]),
                                                                            dbc.Col([dcc.Input(value='0000', type='text', id='dato10', disabled=True, style={'margin-top':'5px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '30px'})]),

                                                                        ]),
                                                                    dbc.Row([dbc.Col([html.H6('Desempeño',style={'margin-top':'10px'})]),
                                                                            dbc.Col([dcc.Input(value='0000', type='text', id='dato11', disabled=True, style={'margin-top':'5px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '30px'})]),

                                                                  ]),

                                                                    dbc.Row([dbc.Col([dcc.Input(value='---', type='text', id='t_deten_3', disabled=True, style={'margin-top':'5px',"width": "100%",  'background-color': ' #5dade2 ','color':'white','text-align': 'left','font-size': '25px'})])]),

                                                            ])],style={"height": "21rem",'border': 'black 2px solid','text-align':'left','margin-top':'10px','margin-left':'10px'}
                                                            )]),
                                    dcc.Interval(id='interval-ultimos-datos', interval=interval, n_intervals=0),
                             ], width=2),
###########################################################################################################################3
                        dbc.Col([dbc.Row([dbc.Col([dcc.Input(value='----', type='text', id='msj1', disabled=True, style={'margin-top':'10px',"width": "100%", "margin-left":'5px' ,'background-color': ' #5dade2 ','color':'white','text-align': 'center','font-size': '35px','font-weight': 'bold'})])]),
                            dbc.Row([dbc.Col([dcc.Graph(id='grafico_1',figure={'layout': {
                                                    'title': f'Línea {nombre_lineas[0]}',
                                                    'height':269,
                                                    'width': 1100,
                                                    'margin': {'l': 40, 'r': 20, 't': 25, 'b': 40},
                                                    'plot_bgcolor': colors['background'],
                                                    'paper_bgcolor': colors['background'],
                                                    'font': {
                                                        'color': colors['text']
                                                    },
                            }}, style={"margin-top":'10px',"margin-left":'5px'}),
                                    dcc.Interval(id='interval-grafico_1', interval=interval, n_intervals=0)])]),
########################################################################################################################
                                 dbc.Row([dbc.Col([dcc.Input(value='----', type='text', id='msj2', disabled=True, style={'margin-top':'10px',"width": "100%", "margin-left":'5px' ,'background-color': ' #5dade2 ','color':'white','text-align': 'center','font-size': '35px','font-weight': 'bold'})])]),
                                dbc.Row([dcc.Graph(id='grafico_2',figure={'layout': {
                                                    'title': f'Línea {nombre_lineas[1]}',
                                                    'height':269,
                                                    'width': 1070,
                                                    'margin': {'l': 40, 'r': 20, 't': 25, 'b': 40},
                                                    'plot_bgcolor': colors['background'],
                                                    'paper_bgcolor': colors['background'],
                                                    'font': {
                                                        'color': colors['text']
                                                    },
                            }}, style={"margin-top":'10px',"margin-left":'5px'}),
                                   dcc.Interval(id='interval-grafico_2', interval=interval, n_intervals=0)]),
#########################################################################################################################
                                 dbc.Row([dbc.Col([dcc.Input(value='----', type='text', id='msj3', disabled=True, style={'margin-top':'10px',"width": "100%", "margin-left":'5px' ,'background-color': ' #5dade2 ','color':'white','text-align': 'center','font-size': '35px','font-weight': 'bold'})])]),
                                dbc.Row([dbc.Col([dcc.Graph(id='grafico_3',figure={'layout': {
                                                    'title': f'Línea {nombre_lineas[2]}',
                                                    'height':269,
                                                    'width': 1070,
                                                    'margin': {'l': 40, 'r': 20, 't': 25, 'b': 40},
                                                    'plot_bgcolor': colors['background'],
                                                    'paper_bgcolor': colors['background'],
                                                    'font': {
                                                        'color': colors['text']
                                                    },
                            }}, style={"margin-top":'10px',"margin-left":'5px'}),
                                   dcc.Interval(id='interval-grafico_3', interval=interval, n_intervals=0),
                                            dcc.Interval(id='interval-op', interval=interval, n_intervals=0)
                                         ])]),
                                 ], width=7),
###################################################################################################################
                        dbc.Col([
                            dbc.Row([
                                dbc.Card([dbc.CardBody([
                                    dbc.Row([dbc.Col([dcc.Input(value='Próxima Fabricación', type='text', id='datox', disabled=True, style={"width": "100%",  'background-color': ' #5dade2 ','color':'white','text-align': 'center','font-size': '25px'})])]),

                                                dbc.Row([dbc.Col([dcc.Textarea(placeholder='',id="text_area_msj1",value='',
                                                     style={"width": "100%", 'margin-top': '10px','margin-bottom':'5px','background-color': 'black', 'color': 'white','text-align': 'center','font-size': '35px','font-weight': 'bold'},
                                                     cols=3, rows=4),])]),





                                ])],style={"height": "21rem","width": "65rem",'border': 'black 2px solid','text-align':'center','margin-top':'10px'}
                                 )
                            ]),
##############################################################################################################################333
                            dbc.Row([
                                    dbc.Card([dbc.CardBody([
                                    dbc.Row([dbc.Col([dcc.Input(value='Próxima Fabricación', type='text', id='datox', disabled=True, style={"width": "100%",  'background-color': ' #5dade2 ','color':'white','text-align': 'center','font-size': '25px'})])]),

                                                dbc.Row([dbc.Col([dcc.Textarea(placeholder='',id="text_area_msj2",value='',
                                                     style={"width": "100%", 'margin-top': '10px','margin-bottom':'5px','background-color': 'black', 'color': 'white','text-align': 'center','font-size': '35px','font-weight': 'bold'},
                                                     cols=3, rows=4),])]),





                                ])],style={"height": "21rem","width": "65rem",'border': 'black 2px solid','text-align':'center','margin-top':'10px'}
                                 )

                            ]),
######################################################################################################################3
                            dbc.Row([
                                    dbc.Card([dbc.CardBody([
                                    dbc.Row([dbc.Col([dcc.Input(value='Próxima Fabricación', type='text', id='datox', disabled=True, style={"width": "100%",  'background-color': ' #5dade2 ','color':'white','text-align': 'center','font-size': '25px'})])]),

                                                dbc.Row([dbc.Col([dcc.Textarea(placeholder='',id="text_area_msj3",value='',
                                                     style={"width": "100%", 'margin-top': '10px','margin-bottom':'5px','background-color': 'black', 'color': 'white','text-align': 'center','font-size': '35px','font-weight': 'bold'},
                                                     cols=3, rows=4),
                                                                  dcc.Interval(id='interval-msjs', interval=interval, n_intervals=0)])]),





                                ])],style={"height": "21rem","width": "65rem",'border': 'black 2px solid','text-align':'center','margin-top':'10px'}
                                 )
                            ])
                        ], width=3),
                        ]),
])
#############################################callback GRAFICO 1

@app.callback(
   Output('grafico_1', 'figure'),
[Input('interval-grafico_1', 'n_intervals')])
def update_valor(id):
    try:
        hora_ini = dat.now()
        url = f"http://{host}:{port}/grafico/&{lineas[0]}"  #tiene 5 dosificadores
        print(url)
        response = requests.get(url)
        salida_json = response.json()
        df = pd.DataFrame(salida_json)
        fecha = dat.now()
        hora_actual = fecha.strftime("%M")
        hora_fin = dat.now()
        #diferencia = (hora_fin.timestamp() - hora_ini.timestamp())

        df['date'] = pd.to_datetime(df['fecha'], unit='ms')


        if lineas[0]==7:
            ultimo_dato = df.tail(1)
            ultimo_set = ultimo_dato.iloc[0, 1].round(1)
            ultimo_flujo = ultimo_dato.iloc[0, 2].round(1)
            df_hora = df.loc[:, 'date']
            r40001 = df.loc[:, 'r40001']
            r40003 = df.loc[:, 'r40003']
            r40009 = df.loc[:, 'r40009']
            r40017 = df.loc[:, 'r40017']
            r40025 = df.loc[:, 'r40025']
            r40033 = df.loc[:, 'r40033']
            r40041 = df.loc[:, 'r40041']
            return {'data': [
                {'x': df_hora, 'y': r40001, 'type': 'line', 'name': 'Set [Kg/h]','line': {'color': 'yellow' }},
                {'x': df_hora, 'y': r40003, 'type': 'line', 'name': ' Real[Kg/h]','line': {'color': 'red' }},
                {'x': df_hora, 'y': r40009, 'type': 'line', 'name': ' D1[Kg/h]', 'line': {'color': 'blue' }},
                {'x': df_hora, 'y': r40017, 'type': 'line', 'name': ' D2[Kg/h', 'line': {'color': 'white'}},
                {'x': df_hora, 'y': r40025, 'type': 'line', 'name': ' D3[Kg/h', 'line': {'color': "magenta"}},
                {'x': df_hora, 'y': r40033, 'type': 'line', 'name': ' D4[Kg/h]', 'line': {'color': "goldenrod"}},
               # {'x': df_hora, 'y': r40041, 'type': 'line', 'name': 'Flujo D5[Kg/h]', 'line': {'color': "green"}},
                ],
            'layout': {
                'yaxis': {'range': range, 'title': 'Flujo Masa [Kg/h]'},
                'xaxis': {'title': 'Tiempo [h]'},
                'title': 'Línea 7',
                'height': 269,
                'width': 1110,
                'margin': {'l': 40, 'r': 20, 't': 25, 'b': 40},
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                },
            }
            }
        elif lineas[0]==1:
            df_hora = df.loc[:, 'date']
            ch1 = df.loc[:, 'ch1']
            ch2 = df.loc[:, 'ch1']
            return {'data': [
                {'x': df_hora, 'y': ch1, 'type': 'line', 'name': 'motor estrusora lin1', 'line': {'color': 'yellow'}},
                {'x': df_hora, 'y': ch1, 'type': 'line', 'name': 'dosificador lin1', 'line': {'color': 'red'}},

            ],
                        'layout': {
                            'yaxis': {'range': range, 'title': 'Flujo Masa [Kg/h]'},
                            'xaxis': {'title': 'Tiempo [h]'},
                            'title': f'Línea {lineas[0]}',
                            'height': 269,
                            'width': 1110,
                            'margin': {'l': 40, 'r': 20, 't': 25, 'b': 40},
                            'plot_bgcolor': colors['background'],
                            'paper_bgcolor': colors['background'],
                            'font': {
                                'color': colors['text']
                            },
                        }
                    }

        else:
            ultimo_dato = df.tail(1)
            ultimo_set = ultimo_dato.iloc[0, 1].round(1)
            ultimo_flujo = ultimo_dato.iloc[0, 2].round(1)
            df_hora = df.loc[:, 'date']
            r40001 = df.loc[:, 'r40001']
            r40003 = df.loc[:, 'r40003']
            r40009 = df.loc[:, 'r40009']
            r40017 = df.loc[:, 'r40017']
            r40025 = df.loc[:, 'r40025']
            return {'data': [
                {'x': df_hora, 'y': r40001, 'type': 'line', 'name': 'Set[Kg/h]', 'line': {'color': 'yellow'}},
                {'x': df_hora, 'y': r40003, 'type': 'line', 'name': ' Real[Kg/h]', 'line': {'color': 'red'}},
                {'x': df_hora, 'y': r40009, 'type': 'line', 'name': ' D1[[Kg/h]', 'line': {'color': 'blue'}},
                {'x': df_hora, 'y': r40017, 'type': 'line', 'name': ' D2[Kg/h', 'line': {'color': 'white'}},
                {'x': df_hora, 'y': r40025, 'type': 'line', 'name': ' D3[Kg/h]', 'line': {'color': "magenta"}},
            ],
                        'layout': {
                            'yaxis': {'range': range, 'title': 'Flujo Masa [Kg/h]'},
                            'xaxis': {'title': 'Tiempo [h]'},
                            'title': f'Línea {lineas[0]}',
                            'height': 269,
                            'width': 1110,
                            'margin': {'l': 40, 'r': 20, 't': 25, 'b': 40},
                            'plot_bgcolor': colors['background'],
                            'paper_bgcolor': colors['background'],
                            'font': {
                                'color': colors['text']
                            },
                        }
                    }

    except:
        return (funcion_except(f'Línea {lineas[0]}'))



#############################################callback GRAFICO 2

@app.callback(
   Output('grafico_2', 'figure'),

[Input('interval-grafico_2', 'n_intervals')])
def update_valor2(id):
    try:
        hora_ini = dat.now()
        url = f"http://{host}:{port}/grafico/&{lineas[1]}"
        print(url)
        response = requests.get(url)
        salida_json = response.json()
        df = pd.DataFrame(salida_json)
        hora_fin = dat.now()
        diferencia = (hora_fin.timestamp() - hora_ini.timestamp())
        df['date'] = pd.to_datetime(df['fecha'], unit='ms')
        print('df2', df)
        if lineas[1]==2:
            df_hora = df.loc[:, 'date']
            ch1 = df.loc[:, 'ch1']
            ch2 = df.loc[:, 'ch1']

            return {'data': [
                {'x': df_hora, 'y': ch1, 'type': 'line', 'name': 'motor principal lin2', 'line': {'color': 'yellow'}},
                {'x': df_hora, 'y': ch1, 'type': 'line', 'name': 'dosificador lin 2', 'line': {'color': 'red'}},

            ],
                        'layout': {
                            'yaxis': {'range': range, 'title': 'Flujo Masa [Kg/h]'},
                            'xaxis': {'title': 'Tiempo [h]'},
                            'title': f'Línea {lineas[1]}',
                            'height': 269,
                            'width': 1110,
                            'margin': {'l': 40, 'r': 20, 't': 25, 'b': 40},
                            'plot_bgcolor': colors['background'],
                            'paper_bgcolor': colors['background'],
                            'font': {
                                'color': colors['text']
                            },
                        }
                    }

        else:
            ultimo_dato = df.tail(1)
            ultimo_set = ultimo_dato.iloc[0, 1].round(1)
            ultimo_flujo=ultimo_dato.iloc[0,2].round(1)
            df_hora=df.loc[:,'date']
            r40001=df.loc[:,'r40001']
            r40003 = df.loc[:, 'r40003']
            r40009 = df.loc[:, 'r40009']
            r40017 = df.loc[:, 'r40017']
            r40025 = df.loc[:, 'r40025']
            return {'data': [
                {'x': df_hora, 'y': r40001, 'type': 'line', 'name': 'Set[Kg/h]','line': {'color': 'yellow' }},
                {'x': df_hora, 'y': r40003, 'type': 'line', 'name': ' Real[Kg/h]','line': {'color': 'red' }},
                {'x': df_hora, 'y': r40009, 'type': 'line', 'name': ' D1[[Kg/h]', 'line': {'color': 'blue' }},
                {'x': df_hora, 'y': r40017, 'type': 'line', 'name': ' D2[Kg/h]', 'line': {'color': 'white'}},
                {'x': df_hora, 'y': r40025, 'type': 'line', 'name': ' D3[Kg/h]', 'line': {'color': "magenta"}},


            ],
                'layout': {
                    'yaxis': {'range': range,'title':'Flujo Masa [Kg/h]'},
                    'xaxis': { 'title': 'Tiempo [h]'},
                    'title': f'Línea {nombre_lineas[1]}',
                    'height':269,
                    'width': 1110,
                    'margin': {'l': 40, 'r': 20, 't': 25, 'b': 40},
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']
                    },

                }
            }
    except:
        return (funcion_except(f'Línea {nombre_lineas[1]}'))


#############################################callback GRAFICO 3

@app.callback(
   Output('grafico_3', 'figure'),

[Input('interval-grafico_3', 'n_intervals')])
def update_valor3(id):
    try:
        hora_ini = dat.now()
        url = f"http://{host}:{port}/grafico/&{lineas[2]}"
        print("grafico 3 es")
        print(url)
        response = requests.get(url)
        salida_json = response.json()
        df = pd.DataFrame(salida_json)
        hora_fin = dat.now()
        diferencia = (hora_fin.timestamp() - hora_ini.timestamp())
        df['date'] = pd.to_datetime(df['fecha'], unit='ms')
        ultimo_dato = df.tail(1)
        ultimo_set = ultimo_dato.iloc[0, 1].round(1)
        ultimo_flujo=ultimo_dato.iloc[0,2].round(1)
        df_hora=df.loc[:,'date']
        r40001=df.loc[:,'r40001']
        r40003 = df.loc[:, 'r40003']
        r40009 = df.loc[:, 'r40009']
        r40017 = df.loc[:, 'r40017']
        r40025 = df.loc[:, 'r40025']
        return {
            'data': [
                {'x': df_hora, 'y': r40001, 'type': 'line', 'name': 'Set[Kg/h','line': {'color': 'yellow' }},
                {'x': df_hora, 'y': r40003, 'type': 'line', 'name': ' Real[Kg/h]','line': {'color': 'red' }},
                {'x': df_hora, 'y': r40009, 'type': 'line', 'name': ' D1[Kg/h]', 'line': {'color': 'blue' }},
                {'x': df_hora, 'y': r40017, 'type': 'line', 'name': ' D2[Kg/h]', 'line': {'color': 'white'}},
                {'x': df_hora, 'y': r40025, 'type': 'line', 'name': ' D3[Kg/h]', 'line': {'color': "magenta"}},
            ],
                'layout': {
                    'yaxis': {'range': range,'title':'Flujo Masa [Kg/h]'},
                    'xaxis': { 'title':'Tiempo [h]'},
                    'title': f'Línea {nombre_lineas[2]}',
                    'height':269,
                    'width': 1110,
                    'margin': {'l': 40, 'r': 20, 't': 25, 'b': 40},
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']
                    },
                }
            }
    except:
        return (funcion_except(f'Línea {nombre_lineas[2]}'))
#####################################################################CALLBACK ULTIMOS DATOS CARD



 ##EGE LINEA 1

@app.callback(
    [Output('dato1', 'value'),
     Output('dato2', 'value'),
     Output('dato3', 'value'),
    Output('rend_teo1', 'children'),
    Output('t_deten_1', 'value'),
    ],
    [Input('interval-ultimos-datos', 'n_intervals')])
def update_ege_1(value):
    print(f"entro a ultimo dato")
    try:
        valor1 = '60 %'
        valor2 = '30 %'
        valor3 = '100 %'
        valor4 = '75 %'
        url = f"http://{host}:{port}/valores_ege/&{lineas[0]}"
        print("+" * 200)
        print(url)
        response = requests.get(url)
        salida_json = response.json()
        json_object = json.loads(salida_json)
        estado = json_object['estado']
        ege = json_object['ege']
        disponib = json_object['disponibilidad']
        desempeno = json_object['desempeno']
        defecto = json_object['defecto']
        rend_teo = json_object['rendimiento_teorico']
        tiempo_det  = json_object['tiempo_detenido']
        estado_pro = json_object['estado_produccion']
        ege_str = str(ege) + '%'
        dispon_str = str(disponib) + '%'
        desempeno_str = str(desempeno) + '%'
        defecto_str = str(defecto) + '%'
        rend_str = str(rend_teo)
        tiempo_str = str(tiempo_det)
        estado_str = str(estado_pro)
        tiempo = 'T. Detenc.: '+ tiempo_str+ '  '+'h:m'

        return ( ege_str, dispon_str, desempeno_str,func_rend_teo_ok(rend_str, estado_str),tiempo)
    except:
        error = '--'
        return (error, error, error,func_rend_teo_error(),error)

##ege 2
@app.callback(
    [Output('ege_ad', 'value'),
     Output('disp_ad', 'value') ,
     Output('desem_ad', 'value'),
     Output('rend_teo2', 'children'),
     Output('t_deten_2', 'value'),
     ],
    [Input('interval-ultimos-datos', 'n_intervals')])
def update_ult_dato(value):
    print(f"entro a ultimo dato")
    try:

        url = f"http://{host}:{port}/valores_ege/&{lineas[1]}"
        print("+"*200)
        print(url)
        response = requests.get(url)
        salida_json = response.json()
        json_object = json.loads(salida_json)
        estado = json_object['estado']
        ege = json_object['ege']
        disponib = json_object['disponibilidad']
        desempeno = json_object['desempeno']
        defecto = json_object['defecto']
        rend_teo = json_object['rendimiento_teorico']
        tiempo_det  = json_object['tiempo_detenido']
        estado_pro = json_object['estado_produccion']
        ege_str = str(ege)+'%'
        dispon_str = str(disponib) + '%'
        desempeno_str = str(desempeno) + '%'
        defecto_str = str(defecto) + '%'
        rend_str = str(rend_teo)
        tiempo_str = str(tiempo_det)
        estado_str = str(estado_pro)
        tiempo = 'T. Detenc.: ' + tiempo_str+ '  '+'h:m'

        return ( ege_str,dispon_str,desempeno_str, func_rend_teo_ok(rend_str,estado_str),tiempo)
    except:
        error='--'
        return (error,error,error, func_rend_teo_error(), error)



##ege 3

@app.callback(
    [Output('dato9', 'value'),
     Output('dato10', 'value'),
     Output('dato11', 'value'),
     Output('rend_teo3', 'children'),
     Output('t_deten_3', 'value'),
     ],
    [Input('interval-ultimos-datos', 'n_intervals')])
def update_ege_3(value):
    print(f"entro a ultimo dato")
    try:
        valor1= '60 %'
        valor2 = '30 %'
        valor3 = '100 %'
        valor4 = '75 %'
        url = f"http://{host}:{port}/valores_ege/&{lineas[2]}"
        print("+"*200)
        print(url)
        response = requests.get(url)
        salida_json = response.json()
        json_object = json.loads(salida_json)
        estado = json_object['estado']
        ege = json_object['ege']
        disponib = json_object['disponibilidad']
        desempeno = json_object['desempeno']
        defecto = json_object['defecto']
        rend_teo = json_object['rendimiento_teorico']
        tiempo_det  = json_object['tiempo_detenido']
        estado_pro = json_object['estado_produccion']
        ege_str = str(ege)+'%'
        dispon_str = str(disponib) + '%'
        desempeno_str = str(desempeno) + '%'
        defecto_str = str(defecto) + '%'
        rend_str = str(rend_teo)
        tiempo_str = str(tiempo_det)
        estado_str = str(estado_pro)
        tiempo = 'T. Detenc.: ' + tiempo_str + ' '+'h:m'
        return ( ege_str, dispon_str, desempeno_str,func_rend_teo_ok(rend_str,estado_str),tiempo)
    except:
        error='--'
        return (error,error,error, func_rend_teo_error(),error)



#####################################################################CALLBACK ULTIMOS MENSAJES PANEL
@app.callback(
    [Output("text_area_msj1", 'value'),
    Output("text_area_msj2", 'value'),
    Output("text_area_msj3", 'value'),
],
    [Input('interval-msjs', 'n_intervals')])
def update_ult_msj_PANEL(value):
    try:
        url7 = f"http://{host}:{port}/mensaje_panel/&{lineas[0]}"


        print("*" * 200)
        print(url7)
        response7 = requests.get(url7)
        salida_json7 = response7.json()
        json_object7 = json.loads(salida_json7)
        mensaje7 = json_object7['mensaje']

        url3 = f"http://{host}:{port}/mensaje_panel/&{lineas[1]}"
        print("*" * 200)
        print(url3)
        response3 = requests.get(url3)
        salida_json3 = response3.json()
        json_object3 = json.loads(salida_json3)
        print('msj',json_object3)
        mensaje3 = json_object3['mensaje']

        url8 = f"http://{host}:{port}/mensaje_panel/&{lineas[2]}"
        print("*" * 200)
        print(url8)
        response8 = requests.get(url8)
        salida_json8 = response8.json()
        json_object8 = json.loads(salida_json8)
        mensaje8 = json_object8['mensaje']

        return (mensaje7, mensaje3, mensaje8)
    except:
        return ('-----','-----','-----')



#####################################################################CALLBACK ULTIMOS MENSAJES OP ACTIVAS
@app.callback(
    [Output('msj1', 'value'),
    Output('msj2', 'value'),
     Output('msj3', 'value'),
],
    [Input('interval-op', 'n_intervals')])
def update_ult_msj_OP_ACTIVAS(value):
    try:
        url7 = f"http://{host}:{port}/op_activas/&{lineas[0]}"


        print("x" * 200)
        print(url7)
        response7 = requests.get(url7)
        salida_json7 = response7.json()
        json_object7 = json.loads(salida_json7)
        mensaje7 = json_object7['op']
        print('op',json_object7)

        url3 = f"http://{host}:{port}/op_activas/&{lineas[1]}"
        print("*" * 200)
        print(url3)
        response3 = requests.get(url3)
        salida_json3 = response3.json()
        json_object3 = json.loads(salida_json3)
        mensaje3 =  json_object3['op']

        url8 = f"http://{host}:{port}/op_activas/&{lineas[2]}"
        print("*" * 200)
        print(url8)
        response8 = requests.get(url8)
        salida_json8 = response8.json()
        json_object8 = json.loads(salida_json8)
        print('jason',json_object8)
        mensaje8 =  json_object8['op']
        return (mensaje7, mensaje3, mensaje8)
    except:
        return ('-----','-----','-----')

################################################ FUNCION RENDIMIENTO TEORICO OK
def func_rend_teo_ok(rend, estado):
    print()
    rendimiento = rend + '  ' + '[Kg/h]'

    if estado == '0':
        back_color = 'green'
    else:
        back_color = 'red'
    return html.Div([dcc.Input(value='Rend Teo:  '+ rendimiento, type='text', id='rend_teo', disabled=True,
                                   style={'margin-top':'5px',"width": "100%",  'background-color': back_color,'color':'white','text-align': 'left','font-size': '25px'})
                         ]),

################################################ FUNCION RENDIMIENTO TEORICO OK
def func_rend_teo_error():
    print()
    return html.Div([dcc.Input(value='Rend Teo:----', type='text', id='rend_teo', disabled=True,
                                   style={'margin-top':'5px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'left','font-size': '25px'})
                         ]),


#####################################################################CALLBACK DIPLAY hora
@app.callback(
    Output('display', 'value'),
    [Input('interval-ultimos-datos', 'n_intervals')])
def update_hora(value):
    try:
        fecha = dat.now()
        hora_actual = fecha.strftime("%H:%M")
        return (hora_actual)
    except:
        return (0.0)


def funcion_except(titulo):
    print()
    datos = {
        'hora': ['00:00', '01:00', '02:00', '03:00'],
        'linea1': [30, 30, 30, 30],
        'linea2': [20, 20, 20, 20],

    }

    df_sin_conexion = pd.DataFrame(datos)
    df_hora = df_sin_conexion.loc[:, 'hora']
    lin1 = df_sin_conexion.loc[:, 'linea1']
    lin2 = df_sin_conexion.loc[:, 'linea2']

    print('df error', df_sin_conexion)
    return {
        'data': [
            {'x': df_hora, 'y': lin1, 'type': 'line', 'name': 'Sin Conexión', 'line': {'color': 'red'}},
            {'x': df_hora, 'y': lin2, 'type': 'line', 'name': 'Sin Conexión', 'line': {'color': 'red'}},

        ],
        'layout': {
            'title': titulo,
            'height': 269,
            'width': 1110,
            'margin': {'l': 40, 'r': 20, 't': 25, 'b': 40},
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['background'],
            'font': {
                'color': colors['text']
            },

        }

    }
