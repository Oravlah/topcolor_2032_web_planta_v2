# index page
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash import dash_table

from server import app, server
from flask_login import logout_user, current_user
import dash_bootstrap_components as dbc
from views import   home_2
from dotenv import load_dotenv
import os

BASEDIR = os.path.dirname(os.path.abspath(__file__))
ENV_VARS = os.path.join(BASEDIR, ".env")
# se cargan las variables de entorno
load_dotenv(ENV_VARS)
########################

port_web = os.environ.get('PUERTO_WEB')


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink(id='home', className='link')),
        dbc.NavItem(dbc.NavLink(id='configuracion', className='link')),
        #dbc.NavItem(dbc.NavLink(id='graficos', className='link')),
        #dbc.NavItem(dbc.NavLink(id='user-name', className='link')),
        #dbc.NavItem(dbc.NavLink(id='logout', className='link')),
        html.Img(src='assets/logovesat.png', height="48px", width='100px', className='logo'),
        dbc.Label("    ", style=dict(marginRight=10)),
        html.Img(src='assets/topcolor.png', height="48px", width='100px', className='logo'),

    ],
    style={'height': 50},

    color= "dark",
    dark=True
)
app.layout = html.Div(
    [
        #navbar,
        html.Div([
            html.Div(
                html.Div(id='page-content', className='content'),
                className='content-container'
            ),
        ], className='container-width'),
        dcc.Location(id='url', refresh=False),
    ]
)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':

        return home_2.layout

    elif pathname == '/home_2':

        return home_2.layout



    else:
        return '404'

#####ACA VAN LOS TITULOS DEL MENU. SOLO APARARECEN CUANDO ESTE LOGUEADO
@app.callback(Output('home', 'children'),[Input('page-content', 'children')])
def user_logout(input1):
    #if current_user.is_authenticated:
    return html.A('Home', href='/home')
    #else:
       # return '        '

@app.callback(Output('configuracion', 'children'),[Input('page-content', 'children')])
def user_logout(input1):
    #if current_user.is_authenticated:
    return html.A('Configuración', href='/configuracion')
    #else:
       # return '        '



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port_web)