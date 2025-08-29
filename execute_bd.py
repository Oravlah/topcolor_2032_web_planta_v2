import pymysql
import random
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table as dt
import plotly.graph_objects as go
from datetime import datetime as dat
import dash_bootstrap_components as dbc
from datetime import date

import clientes_db as cd
import users_mgt as um
import ingreso_motor_bd as ing

#um.create_user_table()

#um.add_user('jose','jose.1','vesat@test.com','admin')
um.add_user('diego','diego.1','diego@test.cl','admin')

#cd.create_cliente_table()

#cd.add_cliente('alvaro','vesat ingenieria','santiago centro','alvaro@vesat.com','+56 912345678')

#ing.create_ingreso_table()