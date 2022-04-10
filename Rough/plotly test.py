#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 13:25:02 2022

@author: vandam
"""
### PACKAGES WE NEED ###
import pandas as pd
import plotly.express as px
import plotly.io as pio
#pio.renderers.default = 'svg'              # NOT WORKING FOR NOW
pio.renderers.default = 'browser'           # Displays the graph in the Browser

# Reads the URL of the CSV file
df = pd.read_csv('https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&areaCode=E06000023&metric=cumPeopleVaccinatedFirstDoseByVaccinationDate&metric=cumPeopleVaccinatedSecondDoseByVaccinationDate&metric=cumPeopleVaccinatedThirdInjectionByVaccinationDate&metric=cumCasesByPublishDate&format=csv')

# Show fig, x axis, y axis, title
fig = px.line(df, x = 'date', y = 'cumCasesByPublishDate', title='Test')
fig.show()