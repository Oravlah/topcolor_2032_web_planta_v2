
import pandas as pd
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

from datetime import datetime as dat
import dash_bootstrap_components as dbc
import json
import requests
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

host_prueba = os.environ.get('IP_API_PRUEBA')
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
##NOTA:
##la linea 3 esta el la tabla de valores en bruto 8, y la linea aditivo esta en la tabla de valores brutos 8.
##pero en las tablas de ops y mensajes esta correcto el orden, por lo que se debe tener cuidad que cuando en la API se solicite el ege de la 3, se debe buscar
##los valores brutos del 8
#linea 1 y 2
if port_web=="8500":
 lineas=[1,2]
 lineas_ege=[1,2]
 linea_ult_op=[1,2]  #lineas que se van a buscas a mensaje de ultima op
 nombre_lineas=[1,2]
 range = [0, 20]

#linea 3 y 4
elif port_web=="8501":
 lineas=[8,4]
 lineas_ege = [3, 4]
 linea_ult_op = [3, 4]  # lineas que se van a buscas a mensaje de ultima op
 nombre_lineas=[3,4]
 range = [0,250]

#linea 5 y 6
elif port_web=="8502":
 lineas=[5,6]
 lineas_ege = [5, 6]
 linea_ult_op = [5, 6]  # lineas que se van a buscas a mensaje de ultima op
 nombre_lineas=[5,6]
 range = [0, 250]

#linea 7 y 8
elif port_web=="8503":
 lineas=[7,10]
 lineas_ege = [7, 10]
 linea_ult_op = [7, 10]  # lineas que se van a buscas a mensaje de ultima op
 nombre_lineas=[7,"8"]
 range = [0, 250]

#linea blanco-aditivo
elif port_web=="8504":
 lineas=[9,3]
 lineas_ege = [9, 8]
 linea_ult_op = [9, 8]  # lineas que se van a buscas a mensaje de ultima op
 nombre_lineas=["blanco","aditivo"]
 range = [0, 700]
#linea 5 y 6


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
                                                    dbc.CardBody([dbc.Row([ dbc.Col([dcc.Input(value=f'Línea {nombre_lineas[0]}', type='text', id='datox', disabled=True, style={"width": "100%",  'background-color': ' #5dade2 ','color':'white','text-align': 'center','font-size': '35px'})])]),
                                                                    dbc.Row([ dbc.Col([dcc.Input(value='Rendimiento Teórico', type='text', id='datox', disabled=True, style={'margin-top':'10px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '25px'})])]),
                                                                  dbc.Row([dbc.Col([html.Div(id='rend_teo1_home2')])]),
                                                                  dbc.Row([dbc.Col([html.H6('EGE',style={'margin-top':'30px'})]),
                                                                            dbc.Col([dcc.Input(value='0000', type='text', id='dato1_home2', disabled=True, style={'margin-top':'20px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '30px'})]),

                                                                           ]),
                                                                  dbc.Row([dbc.Col([html.H6('Disponibilidad',style={'margin-top':'30px'})]),
                                                                            dbc.Col([dcc.Input(value='0000', type='text', id='dato2_home2', disabled=True, style={'margin-top':'20px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '30px'})]),

                                                                        ]),
                                                                    dbc.Row([dbc.Col([html.H6('Desempeño',style={'margin-top':'30px'})]),
                                                                            dbc.Col([dcc.Input(value='0000', type='text', id='dato3_home2', disabled=True, style={'margin-top':'20px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '30px'})]),

                                                                  ]),
                                                                    dbc.Row([dbc.Col([html.H6('T.Detención',style={'margin-top':'30px'})]),
                                                                        dbc.Col([dcc.Input(value='---', type='text', id='t_deten_1_home2', disabled=True, style={'margin-top':'20px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '30px'})])]),


                                                            ])],style={"height": "33rem",'border': 'black 2px solid','text-align':'left','margin-left':'10px','margin-top':'10px'}
                                                            )]),
################################################################################################################################3
                                        dbc.Row([dbc.Card([
                                                dbc.CardBody([dbc.Row([dbc.Col([dcc.Input(value=f'Línea {nombre_lineas[1]}', type='text', id='datox', disabled=True, style={"width": "100%",  'background-color': ' #5dade2 ','color':'white','text-align': 'center','font-size': '35px'})])]),
                                                            dbc.Row([ dbc.Col([dcc.Input(value='Rendimiento Teórico', type='text', id='datox', disabled=True, style={'margin-top':'10px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '25px'})])]),
                                                              dbc.Row([dbc.Col([html.Div(id='rend_teo2_home2')])]),
                                                                  dbc.Row([dbc.Col([html.H6('EGE',style={'margin-top':'30px'})]),
                                                                            dbc.Col([dcc.Input(value='0000', type='text', id='ege_ad_home2', disabled=True, style={'margin-top':'20px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '30px'})]),

                                                                           ]),
                                                                  dbc.Row([dbc.Col([html.H6('Disponibilidad',style={'margin-top':'30px'})]),
                                                                            dbc.Col([dcc.Input(value='0000', type='text', id='disp_ad_home2', disabled=True, style={'margin-top':'20px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '30px'})]),

                                                                        ]),
                                                                    dbc.Row([dbc.Col([html.H6('Desempeño',style={'margin-top':'30px'})]),
                                                                            dbc.Col([dcc.Input(value='0000', type='text', id='desem_ad_home2', disabled=True, style={'margin-top':'20px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '30px'})]),

                                                                  ]),

                                                                    dbc.Row([dbc.Col([html.H6('T.Detención',style={'margin-top':'30px'})]),
                                                                        dbc.Col([dcc.Input(value='---', type='text', id='t_deten_2_home2', disabled=True, style={'margin-top':'20px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '30px'})])]),

                                                            ])],style={"height": "33rem",'border': 'black 2px solid','text-align':'left','margin-top':'10px','margin-left':'10px'}
                                                            )]),
##########################################################################################################################

                                    dcc.Interval(id='interval-ultimos-datos_home2', interval=interval, n_intervals=0),
                             ], width=2),
###########################################################################################################################3
                        dbc.Col([dbc.Row([dbc.Col([dcc.Input(value='----', type='text', id='msj1_home2', disabled=True, style={'margin-top':'20px',"width": "100%", "margin-left":'5px' ,'background-color': ' #5dade2 ','color':'white','text-align': 'center','font-size': '45px','font-weight': 'bold'})])]),
                            dbc.Row([dbc.Col([dcc.Graph(id='grafico_1_home2',figure={'layout': {
                                                    'title': f'',
                                                    'height':425,
                                                    'width': 1100,
                                                    'margin': {'l': 40, 'r': 20, 't': 25, 'b': 40},
                                                    'plot_bgcolor': colors['background'],
                                                    'paper_bgcolor': colors['background'],
                                                    'font': {
                                                        'color': colors['text']
                                                    },
                            }}, style={"margin-top":'15px',"margin-left":'5px'}),
                                    dcc.Interval(id='interval-grafico_1_home2', interval=interval, n_intervals=0)])]),
########################################################################################################################
                                 dbc.Row([dbc.Col([dcc.Input(value='----', type='text', id='msj2_home2', disabled=True, style={'margin-top':'20px',"width": "100%", "margin-left":'5px' ,'background-color': ' #5dade2 ','color':'white','text-align': 'center','font-size': '45px','font-weight': 'bold'})])]),
                                dbc.Row([dcc.Graph(id='grafico_2_home2',figure={'layout': {
                                                    'title': f'',
                                                    'height':425,
                                                    'width': 1100,
                                                    'margin': {'l': 40, 'r': 20, 't': 25, 'b': 40},
                                                    'plot_bgcolor': colors['background'],
                                                    'paper_bgcolor': colors['background'],
                                                    'font': {
                                                        'color': colors['text']
                                                    },
                            }}, style={"margin-top":'15px',"margin-left":'5px'}),
                                   dcc.Interval(id='interval-grafico_2_home2', interval=interval, n_intervals=0)]),
                                 dcc.Interval(id='interval-op_home2', interval=interval, n_intervals=0)
#########################################################################################################################

                                 ], width=7),
###################################################################################################################
                        dbc.Col([
                            dbc.Row([
                                dbc.Card([dbc.CardBody([
                                    dbc.Row([dbc.Col([dcc.Input(value='Próxima Fabricación', type='text', id='datox', disabled=True, style={"width": "100%",  'background-color': ' #5dade2 ','color':'white','text-align': 'center','font-size': '35px'})])]),

                                                dbc.Row([dbc.Col([dcc.Textarea(placeholder='',id="text_area_msj1_home2",value='',
                                                     style={"width": "100%", 'margin-top': '10px','margin-bottom':'5px','background-color': 'black', 'color': 'white','text-align': 'center','font-size': '40px','font-weight': 'bold'},
                                                     cols=3, rows=7),])]),





                                ])],style={"height": "33rem","width": "65rem",'border': 'black 2px solid','text-align':'center','margin-top':'10px'}
                                 )
                            ]),
##############################################################################################################################333
                            dbc.Row([
                                    dbc.Card([dbc.CardBody([
                                    dbc.Row([dbc.Col([dcc.Input(value='Próxima Fabricación', type='text', id='datox', disabled=True, style={"width": "100%",  'background-color': ' #5dade2 ','color':'white','text-align': 'center','font-size': '35px'})])]),

                                                dbc.Row([dbc.Col([dcc.Textarea(placeholder='',id="text_area_msj2_home2",value='',
                                                     style={"width": "100%", 'margin-top': '10px','margin-bottom':'5px','background-color': 'black', 'color': 'white','text-align': 'center','font-size': '40px','font-weight': 'bold'},
                                                     cols=3, rows=7),])]),dcc.Interval(id='interval-msjs_home2', interval=interval, n_intervals=0)





                                ])],style={"height": "33rem","width": "65rem",'border': 'black 2px solid','text-align':'center','margin-top':'10px'}
                                 )

                            ]),
######################################################################################################################3

                        ], width=3),
                        ]),
])
#############################################callback GRAFICO 1

@app.callback(
   Output('grafico_1_home2', 'figure'),
[Input('interval-grafico_1_home2', 'n_intervals')])
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
        print("para el segundo grafico es ")
        print(df.head(5))


        if lineas[0]==7:
            range=[0,300]
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
                'title': '',
                'height': 425,
                'width': 1110,
                'margin': {'l': 40, 'r': 20, 't': 25, 'b': 40},
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                },
            }
            }
        ##para linea 8, que son la linea real 3
        elif lineas[0]==8:
            print("Es una linea 3, pero de la tabla 8")
            range=[0,200]
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
                {'x': df_hora, 'y': r40001, 'type': 'line', 'name': 'Set [Kg/h]','line': {'color': 'yellow' }},
                {'x': df_hora, 'y': r40003, 'type': 'line', 'name': ' Real[Kg/h]','line': {'color': 'red' }},
                {'x': df_hora, 'y': r40009, 'type': 'line', 'name': ' D1[Kg/h]', 'line': {'color': 'blue' }},
                {'x': df_hora, 'y': r40017, 'type': 'line', 'name': ' D2[Kg/h', 'line': {'color': 'white'}},
                {'x': df_hora, 'y': r40025, 'type': 'line', 'name': ' D3[Kg/h', 'line': {'color': "magenta"}},],
            'layout': {
                'yaxis': {'range': range, 'title': 'Flujo Masa [Kg/h]'},
                'xaxis': {'title': 'Tiempo [h]'},
                'title': '',
                'height': 425,
                'width': 1110,
                'margin': {'l': 40, 'r': 20, 't': 25, 'b': 40},
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                },
            }
            }

        elif lineas[0]==5:
            print("Es una linea 3, pero de la tabla 8")
            range=[0,150]
            ultimo_dato = df.tail(1)
            ultimo_set = ultimo_dato.iloc[0, 1].round(1)
            ultimo_flujo = ultimo_dato.iloc[0, 2].round(1)
            df_hora = df.loc[:, 'date']
            r40001 = df.loc[:, 'r40001']
            r40003 = df.loc[:, 'r40003']
            r40009 = df.loc[:, 'r40009']
            r40017 = df.loc[:, 'r40017']

            return {'data': [
                {'x': df_hora, 'y': r40001, 'type': 'line', 'name': 'Set [Kg/h]','line': {'color': 'yellow' }},
                {'x': df_hora, 'y': r40003, 'type': 'line', 'name': ' Real[Kg/h]','line': {'color': 'red' }},
                {'x': df_hora, 'y': r40009, 'type': 'line', 'name': ' D1[Kg/h]', 'line': {'color': 'blue' }},
                {'x': df_hora, 'y': r40017, 'type': 'line', 'name': ' D2[Kg/h', 'line': {'color': 'white'}},],
            'layout': {
                'yaxis': {'range': range, 'title': 'Flujo Masa [Kg/h]'},
                'xaxis': {'title': 'Tiempo [h]'},
                'title': '',
                'height': 425,
                'width': 1110,
                'margin': {'l': 40, 'r': 20, 't': 25, 'b': 40},
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                },
            }
            }
        elif lineas[0]==9:
            range=[0,20]
            df_hora = df.loc[:, 'date']
            ch1 = df.loc[:, 'ch1']
            ch2 = df.loc[:, 'ch2']
            ch3 = df.loc[:, 'ch3']
            return {'data': [
                {'x': df_hora, 'y': ch1, 'type': 'line', 'name': 'Extrusora', 'line': {'color': 'yellow'}},
                {'x': df_hora, 'y': ch2, 'type': 'line', 'name': 'Gala', 'line': {'color': 'red'}},

            ],
                        'layout': {
                            'yaxis': {'range': range, 'title': 'Flujo Masa [Kg/h]'},
                            'xaxis': {'title': 'Tiempo [h]'},
                            'title': f'',
                            'height': 425,
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
            range = [0, 20]
            df_hora = df.loc[:, 'date']
            ch1 = df.loc[:, 'ch1']
            ch2 = df.loc[:, 'ch2']
            return {'data': [
                {'x': df_hora, 'y': ch1, 'type': 'line', 'name': 'motor estrusora lin1', 'line': {'color': 'yellow'}},
                {'x': df_hora, 'y': ch2, 'type': 'line', 'name': 'dosificador lin1', 'line': {'color': 'red'}},

            ],
                        'layout': {
                            'yaxis': {'range': range, 'title': 'Flujo Masa [Kg/h]'},
                            'xaxis': {'title': 'Tiempo [h]'},
                            'title': f'',
                            'height': 425,
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
            range=[0,200]
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
                            'title': f'',
                            'height': 425,
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
        return (funcion_except_home2(f'Línea {lineas[0]}'))



#############################################callback GRAFICO 2

@app.callback(
   Output('grafico_2_home2', 'figure'),

[Input('interval-grafico_2_home2', 'n_intervals')])
def update_valor2(id):
    try:
        if(lineas[1]==4):
            range=[0,100]
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
            range=[0,20]
            df_hora = df.loc[:, 'date']
            ch1 = df.loc[:, 'ch1']
            ch2 = df.loc[:, 'ch2']

            return {'data': [
                {'x': df_hora, 'y': ch1, 'type': 'line', 'name': 'motor principal lin2', 'line': {'color': 'yellow'}},
                {'x': df_hora, 'y': ch2, 'type': 'line', 'name': 'dosificador lin 2', 'line': {'color': 'red'}},

            ],
                        'layout': {
                            'yaxis': {'range': range, 'title': 'Flujo Masa [Kg/h]'},
                            'xaxis': {'title': 'Tiempo [h]'},
                            'title': f'',
                            'height': 425,
                            'width': 1110,
                            'margin': {'l': 40, 'r': 20, 't': 25, 'b': 40},
                            'plot_bgcolor': colors['background'],
                            'paper_bgcolor': colors['background'],
                            'font': {
                                'color': colors['text']
                            },
                        }
                    }
            ##aditivo
        elif lineas[1] == 3:
            range = [0, 750]
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
                    'title': f'',
                    'height': 425,
                    'width': 1110,
                    'margin': {'l': 40, 'r': 20, 't': 25, 'b': 40},
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']
                    },
                }
            }
        elif lineas[1]==10:
            range = [0, 20]
            df_hora = df.loc[:, 'date']
            ch1 = df.loc[:, 'ch1']
            ch2 = df.loc[:, 'ch2']
            return {'data': [
                {'x': df_hora, 'y': ch1, 'type': 'line', 'name': 'gala', 'line': {'color': 'yellow'}},
                {'x': df_hora, 'y': ch2, 'type': 'line', 'name': 'extrusora', 'line': {'color': 'red'}},

            ],
                        'layout': {
                            'yaxis': {'range': range, 'title': 'Flujo Masa [Kg/h]'},
                            'xaxis': {'title': 'Tiempo [h]'},
                            'title': f'',
                            'height': 425,
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
            range=[0,200]
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
                    'title': f'',
                    'height':425,
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
        return (funcion_except_home2(f'Línea {nombre_lineas[1]}'))

#####################################################################CALLBACK ULTIMOS DATOS CARD



 ##EGE LINEA 1

@app.callback(
    [Output('dato1_home2', 'value'),
     Output('dato2_home2', 'value'),
     Output('dato3_home2', 'value'),
    Output('rend_teo1_home2', 'children'),
    Output('t_deten_1_home2', 'value'),
    ],
    [Input('interval-ultimos-datos_home2', 'n_intervals')])
def update_ege_1_home2(value):
    print(f"entro a ultimo dato")
    try:
        valor1 = '60 %'
        valor2 = '30 %'
        valor3 = '100 %'
        valor4 = '75 %'
        url = f"http://{host}:{port}/valores_ege/&{lineas_ege[0]}"
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
        tiempo = tiempo_str+ '  '+'hr'

        return ( ege_str, dispon_str, desempeno_str,func_rend_teo_ok_home2(rend_str, estado_str),tiempo)
    except:
        error = '--'
        return (error, error, error,func_rend_teo_error_home2(),error)

##ege 2
@app.callback(
    [Output('ege_ad_home2', 'value'),
     Output('disp_ad_home2', 'value') ,
     Output('desem_ad_home2', 'value'),
     Output('rend_teo2_home2', 'children'),
     Output('t_deten_2_home2', 'value'),
     ],
    [Input('interval-ultimos-datos_home2', 'n_intervals')])
def update_ult_dato_home2(value):
    print(f"entro a ultimo dato")
    try:

        url = f"http://{host}:{port}/valores_ege/&{lineas_ege[1]}"
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
        tiempo = tiempo_str+ '  '+'hr'
        return ( ege_str,dispon_str,desempeno_str, func_rend_teo_ok_home2(rend_str,estado_str),tiempo)
    except:
        error='--'
        return (error,error,error, func_rend_teo_error_home2(), error)


#####################################################################CALLBACK ULTIMOS MENSAJES PANEL
@app.callback([Output("text_area_msj1_home2", 'value'),Output("text_area_msj2_home2", 'value'),],[Input('interval-msjs_home2', 'n_intervals')])
def update_ult_msj_PANEL_home2(value):
    try:

        ##esto es por las lineas cambiadas de 3 a 8
        if lineas[0]==3:
            url7 = f"http://{host}:{port}/mensaje_panel/&{8}"
        elif lineas[0]==8:
            url7 = f"http://{host}:{port}/mensaje_panel/&{3}"
        else:
            url7 = f"http://{host}:{port}/mensaje_panel/&{lineas[0]}"


        #print("*" * 200)
        #print(url7)
        response7 = requests.get(url7)
        salida_json7 = response7.json()
        json_object7 = json.loads(salida_json7)
        mensaje7 = json_object7['mensaje']

        ##esto es por las lineas cambiadas de 3 a 8
        if lineas[1] == 3:
            url3 = f"http://{host}:{port}/mensaje_panel/&{8}"
        elif lineas[1] == 8:
            url3 = f"http://{host}:{port}/mensaje_panel/&{3}"
        else:
            url3 = f"http://{host}:{port}/mensaje_panel/&{lineas[1]}"


        #print("*" * 200)
        #print(url3)
        response3 = requests.get(url3)
        salida_json3 = response3.json()
        json_object3 = json.loads(salida_json3)
       # print('msj',json_object3)
        mensaje3 = json_object3['mensaje']



        return (mensaje7, mensaje3)
    except:
        return ('-----','-----')


###############  ACA SE DEBE NORMALIZAR LA API YA QUE ESTA API ES SOLO DE PRUEBA ###############################

#####################################################################CALLBACK ULTIMOS MENSAJES OP ACTIVAS
@app.callback(
    [Output('msj1_home2', 'value'),
    Output('msj2_home2', 'value'),
],
    [Input('interval-op_home2', 'n_intervals')])
def update_ult_msj_OP_ACTIVAS_home2(value):
    try:
        url7 = f"http://{host}:{port}/op_activas_json/&{linea_ult_op[0]}"  # API SOLO DE PRUEBA #####
        print("x" * 100+" op activa panel sup "+"*"*100)
        print(url7)
        response7 = requests.get(url7)
        print(f"el response7 es {response7}")
        salida_json7 = response7.json()
        print(f"la salida salida_json7 es {salida_json7}")
        json_object7 = json.loads(salida_json7)
        print(json_object7)
        mensaje7 = json_object7['producto']
        mensaje7_1 = json_object7['op']
        mensaje7_2 = json_object7['rendimiento']
        mensaje7_3 = json_object7['fecha']# API CAMPO SOLO DE PRUEBA #####
        print('op',json_object7)

        url3 = f"http://{host}:{port}/op_activas_json/&{linea_ult_op[1]}"    # API SOLO DE PRUEBA #####
        print("x" * 100+" op activa panel inferior "+"*"*100)
        print(url3)
        response3 = requests.get(url3)
        salida_json3 = response3.json()
        print(salida_json3)
        json_object3 = json.loads(salida_json3)
        print(json_object3)
        mensaje3 = json_object3['producto']
        mensaje3_1 = json_object3['op']
        mensaje3_2 = json_object3['rendimiento']
        mensaje3_3 = json_object3['fecha']  # API CAMPO SOLO DE PRUEBA #####
        print('op', json_object3)
        print(f"los mensajes son {mensaje7}     {mensaje3}")

        return (mensaje7, mensaje3)
    except:
        return ('-+++--','-++--')

################################################ FUNCION RENDIMIENTO TEORICO OK
def func_rend_teo_ok_home2(rend, estado):
    print()
    rendimiento = rend + '  ' + '[Kg/h]'

    if estado == '0':
        back_color = 'green'
    else:
        back_color = 'red'
    return html.Div([dcc.Input(value=rendimiento, type='text', id='rend_teo', disabled=True,
                                   style={'margin-top':'5px',"width": "100%",  'background-color': back_color,'color':'white','text-align': 'center','font-size': '35px'})
                         ]),

################################################ FUNCION RENDIMIENTO TEORICO OK
def func_rend_teo_error_home2():
    print()
    return html.Div([dcc.Input(value='----', type='text', id='rend_teo', disabled=True,
                                   style={'margin-top':'5px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '35px'})
                         ]),


#####################################################################CALLBACK DIPLAY hora
@app.callback(
    Output('display_home2', 'value'),
    [Input('interval-ultimos-datos_home2', 'n_intervals')])
def update_hora(value):
    try:
        fecha = dat.now()
        hora_actual = fecha.strftime("%H:%M")
        return (hora_actual)
    except:
        return (0.0)


def funcion_except_home2(titulo):
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
