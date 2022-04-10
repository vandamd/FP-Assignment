#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 20:40:26 2022

@author: vandam
"""

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from datetime import date
import re
import plotly.io as pio
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)



# URL of CSV
url = 'https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&metric=cumCasesBySpecimenDate&metric=cumPeopleVaccinatedFirstDoseByVaccinationDate&metric=cumPeopleVaccinatedSecondDoseByVaccinationDate&metric=newCasesBySpecimenDate&metric=cumPeopleVaccinatedThirdInjectionByVaccinationDate&format=csv'


# Read CSV
df = pd.read_csv(url)

# Determining the maximum date range - YYYY-MM-DD
dMin_value, dMax_value = df['date'].min(), df['date'].max()



#!# BUG WITH DASH PLOTLY #!#
# Renaming cities with commas
df.replace(to_replace ="Armagh City, Banbridge and Craigavon", 
                 value = "Armagh City and Banbridge and Craigavon", 
                  inplace = True)
df.replace(to_replace ="Bristol, City of", 
                 value = "Bristol", 
                  inplace = True)
df.replace(to_replace ="Bournemouth, Christchurch and Poole", 
                 value = "Bournemouth and Christchurch and Poole", 
                  inplace = True)
df.replace(to_replace ="Herefordshire, County of", 
                 value = "Herefordshire", 
                  inplace = True)
df.replace(to_replace ="Kingston upon Hull, City of", 
                 value = "Kingston upon Hull", 
                  inplace = True)
df.replace(to_replace ="Newry, Mourne and Down", 
                 value = "Newry and Mourne and Down", 
                  inplace = True)


# City list
areaList = sorted(list(set(df['areaName'].tolist())))






### LAYOUT ###

style_dict = dict(width='100%',
                  # border='1.5px black solid',
                  height='50px',
                  # textAlign='center',
                  fontFamily='HelveticaNeue',
                  fontSize=20)

style_dict1 = dict(
                  # border='1.5px black solid',
                  # height='50px',
                  textAlign='center',
                  fontFamily='HelveticaNeue',
                  )


app.layout = html.Div(children=[
    html.H1(children='COVID-19 Data', style=style_dict1),

    html.Div(children='A web application for COVID-19 Data using Dash Plotly.' 
             ' Made by Bayan, Elias, Margherita and Vandam.', 
             style=style_dict1),
    
    # Placeholder
    html.Div(style={'width': '2%', 'display': 'inline-block'}),
    
    # Placeholder
    html.Div(style={'width': '50%', 'display': 'flex'}),
    
    # City Selection Dropdown
    
    
    
    html.Div(
        dcc.Dropdown(
            areaList,
            ['Bristol, City of'],
            id='city-dropdown',
            multi=True,
            style=style_dict,
        ), 
        style={'width': '40%', 'display': 'flex', 'vertical-align': 'top', 'margin-left': 'auto', 'margin-right': 'auto'}
        ),
    
    # Placeholder
    html.Div(style={'width': '2%', 'display': 'inline-block', 'vertical-align': 'top'}),
    
    # Date Range Picker
    html.Div(
        dcc.DatePickerRange(
            id='date-range-picker',
            min_date_allowed=date(int(dMin_value[0:4]), int(dMin_value[5:7]), int(dMin_value[8:10])),
            max_date_allowed=date(int(dMax_value[0:4]), int(dMax_value[5:7]), int(dMax_value[8:10])),
            end_date=date(int(dMax_value[0:4]), int(dMax_value[5:7]), int(dMax_value[8:10])),
            style=style_dict,
        ), 
        style={'width': '14%', 'display': 'flex', 'vertical-align': 'top', 'margin-left': 'auto', 'margin-right': 'auto', 'flex-direction': 'row'}
        ),
    
    # dcc.Graph(
    #     id='example-graph',
    #     figure=fig
    # )
])
                   

if __name__ == '__main__':
    app.run_server(debug=True)
