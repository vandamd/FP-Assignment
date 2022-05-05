#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  4 19:19:19 2022

@author: vandam
"""

from datetime import date
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.express as px
import requests
import json


# CSV of Data
url = 'https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&metric=cumCasesBySpecimenDate&metric=cumPeopleVaccinatedFirstDoseByVaccinationDate&metric=cumPeopleVaccinatedSecondDoseByVaccinationDate&metric=newCasesBySpecimenDate&metric=cumPeopleVaccinatedThirdInjectionByVaccinationDate&format=csv'

# Geojson of the UK
polygons_path = 'UK.geojson'
with open(polygons_path) as p:
    polygons = json.load(p)


# New Cases and Vaccine Doses Function
def showCV (city, start_date, end_date):
    df = pd.read_csv(url)
    df_filtered = df[df['areaName'].str.contains(r'\b' + city + r'\b')]
    
    colorsTotalCases = ['#ff002b', '#0077b6']        #light     red-blue
    colorsNewCases =  ['#c00021', '#023e8a']         #dark      red-blue
    colorsVacc1 = ['#ff6000', '#004b23']             #dark      orange-green
    colorsVacc2 = ['#ff7900', '#38b000']             #mid       orange-green
    colorsVacc3 = ['#ffd000', '#9ef01a']             #light     orange-green

    fig = make_subplots(
        rows=2, cols=2,
        shared_xaxes=True,
        vertical_spacing=0.2,
        column_widths=[1, 1],
        row_heights=[1, 1],
        subplot_titles=("COVID-19 Cases", "Vaccine Doses"),
        specs=[[{"secondary_y": True, "colspan": 2}, None],
               [{"type": "scatter", "colspan": 2}, None]])

    # Graph of Cumulative Cases against Time (1)
    fig.add_trace(
        go.Scatter(
            x=df_filtered["date"],
            y=df_filtered['cumCasesBySpecimenDate'],
            mode="lines",
            name="Total Cases for " + str(city),
            line=dict(color=colorsTotalCases[0])
        ),
        row=1, col=1
    )

    # Graph of New Cases against Time - on top of (1)
    fig.add_trace(
        go.Scatter(
            x=df_filtered["date"],
            y=df_filtered['newCasesBySpecimenDate'],
            name="New Cases for " + str(city),
            line=dict(color=colorsNewCases[0])),
        secondary_y=True,
        row=1, col=1
    )

    # Graph of First Vaccine Doses against Time
    fig.add_trace(
        go.Scatter(
            x=df_filtered["date"],
            y=df_filtered['cumPeopleVaccinatedFirstDoseByVaccinationDate'],
            mode="lines",
            name="First Dose for " + str(city),
            line=dict(color=colorsVacc1[0])
        ),
        row=2, col=1
    )

    # Graph of Second Vaccine Doses against Time
    fig.add_trace(
        go.Scatter(
            x=df_filtered["date"],
            y=df_filtered['cumPeopleVaccinatedSecondDoseByVaccinationDate'],
            name="Second Dose for " + str(city),
            line=dict(color=colorsVacc2[0])
        ),
        row=2, col=1
    )

    # Graph of Third Vaccine Doses against Time
    fig.add_trace(
        go.Scatter(
            x=df_filtered["date"],
            y=df_filtered['cumPeopleVaccinatedThirdInjectionByVaccinationDate'],
            name="Third Dose for " + str(city),
            line=dict(color=colorsVacc3[0])
        ),
        row=2, col=1
    )

    # Figure Formatting
    fig.update_yaxes(title_text="Cumulative COVID-19 Cases", row=1, col=1)     # Title of Left Y-Axis of Cases Graph
    fig.update_yaxes(title_text="New Cases", row=1, col=1, secondary_y=True)   # Title of Right Y-Axis of Cases Graph
    fig.update_yaxes(title_text="Vaccine Doses", row=2, col=1)                 # Title of Y-Axis of Vaccine Graph
    fig.update_xaxes(title_text="Date", row=2, col=1)                          # Title of X-Axis of Vaccine Graphs
    fig.update_xaxes(matches='x')                                              # Allows Cases and Vaccine Graph to zoom together
    fig.update_layout(height=600, autosize=True)                              # Height of the Final Graph
    fig.update_layout(xaxis1_rangeslider_visible=False)                        # Hides Range Slider for Cases Graph
    fig.update_xaxes(rangeslider_thickness = 0.05)                             # Makes Range Slider Shorter
    fig.update_layout(xaxis_range=[start_date, end_date])                      # Update Date using Date Range Picker
    fig.update_layout(hovermode="x unified")                                   # Hover Label
    fig.update_layout(hoverlabel_namelength=-1)                                # Prevents abbreviation of Hover Label

    # Range Slider and Buttons
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month",
                             stepmode="backward"),
                        dict(count=6, label="6m", step="month",
                             stepmode="backward"),
                        dict(count=1, label="1y", step="year",
                             stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            type="date",
        ),
        xaxis2=dict(
            rangeslider=dict(visible=True),
            type="date",
        )
    )
    
    fig.show()


# Show Pie Chart
def showP(city):
    df = pd.read_csv(url)
    df_filtered = df[df['areaName'].str.contains(r'\b' + city + r'\b')]
    df_reset = df_filtered.reset_index(drop=True)
    
    colorsPie1 = ['#ff6000', '#ff7900', '#ffd000']   #orange    dark-light
    
    first_dose_people = df_reset.loc[0, 'cumPeopleVaccinatedFirstDoseByVaccinationDate']
    second_dose_people = df_reset.loc[0, 'cumPeopleVaccinatedSecondDoseByVaccinationDate']
    third_dose_people = df_reset.loc[0, 'cumPeopleVaccinatedThirdInjectionByVaccinationDate']
    
    values = [first_dose_people, second_dose_people, third_dose_people]
    
    
    fig = make_subplots(
        rows=1, cols=2,
        shared_xaxes=True,
        vertical_spacing=0.08,
        column_widths=[1, 1],
        row_heights=[1],
        specs=[[{"type": "pie", "colspan": 2}, None]])

    fig.add_trace(
              go.Pie(
                  title = 'Vaccine Doses in '+ city,
                  labels=['First Dose', 'Second Dose', 'Third Injection'],
                  values=values,
                  textinfo='label+percent',
                  marker=dict(
                      colors=colorsPie1,line=dict(color='#000000', width=0.2)),
                  pull=[0, 0, 0],
                  # name="Vaccine Doses",
                  showlegend = False,),
              row=1, col=1)

    # Figure Formatting
    fig.update_layout(height=500, autosize=True)                              # Height of the Final Graph
    fig.show()




# Show Choropleth Map
def showCh():
    df = pd.read_csv(url)
    df["date2"] = pd.to_datetime(df['date'])
    df = df[df['date2'].dt.day == 1]

    fig1 = px.choropleth_mapbox(
        df.iloc[::-1],
        geojson=polygons,
        locations='areaCode',
        featureidkey="properties.CTYUA21CD",
        color='newCasesBySpecimenDate',
        color_continuous_scale="Reds",
        range_color=(0, 3000),
        hover_name='areaName',
        labels={"newCasesBySpecimenDate": "Cases"},
        animation_frame="date",
        animation_group="areaCode",
        center={"lat": 54.768483, "lon": -4.417318},
        mapbox_style="carto-positron", zoom=5
    )

    fig1.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig1.update_geos(fitbounds="geojson", visible=False)
    fig1.update_layout(height=900, autosize=True)
    return fig1