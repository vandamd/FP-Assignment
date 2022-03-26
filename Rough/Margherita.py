# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import os
import plotly.express as px

df = pd.read_csv('https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&areaCode=S12000033&metric=cumCasesByPublishDate&metric=cumPeopleVaccinatedFirstDoseByVaccinationDate&metric=cumPeopleVaccinatedSecondDoseByVaccinationDate&metric=cumPeopleVaccinatedThirdInjectionByVaccinationDate&format=csv')
print(df)

start_date = input('Input desired start date as follows(YYYY-MM-DD):' )
end_date = input('Input desired end date as follows(YYYY-MM-DD):' )

#date = (start_date <= df['date']) & (df['date'] <= end_date)
    
# Show fig, x axis, y axis 
fig = px.line(df, x = 'date', y = ['cumCasesByPublishDate','cumPeopleVaccinatedFirstDoseByVaccinationDate','cumPeopleVaccinatedSecondDoseByVaccinationDate','cumPeopleVaccinatedThirdInjectionByVaccinationDate'])
fig.update_layout(xaxis_range=[start_date,end_date])
fig.show()








# df = pd.read_csv('https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&metric=cumCasesBySpecimenDate&metric=cumPeopleVaccinatedFirstDoseByVaccinationDate&metric=cumPeopleVaccinatedSecondDoseByVaccinationDate&metric=cumPeopleVaccinatedThirdInjectionByVaccinationDate&format=csv')
# print(df)


# for f in os.listdir('/Users/margheritaparimbelli/Documents/FP_Assignment/'):
#     print(f)

# data = pd.read_csv ('/Users/margheritaparimbelli/Documents/FP_Assignment/BristolVacc.csv', sep = ',')

# df = px.data.gapminder().query()

# x = data['date']
# y = data['cumCasesByPublishDate']

# data.plot(x, y)

# plt.title('Cases according to dates', fontsize = 12)
# plt.xlabel('Dates', fontsize = 12)
# plt.ylabel('Cases numbers', fontsize = 12)
# plt.grid(True)

# print(df)

# df.info()

# df.shape 

# df.isnull().any()

# df['price']
