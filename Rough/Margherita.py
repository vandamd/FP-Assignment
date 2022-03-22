# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import os
import plotly.express as px

for f in os.listdir('/Users/margheritaparimbelli/Documents/FP_Assignment/'):
    print(f)

data = pd.read_csv ('/Users/margheritaparimbelli/Documents/FP_Assignment/BristolVacc.csv', sep = ',')

df = px.data.gapminder().query()

x = data['date']
y = data['cumCasesByPublishDate']

data.plot(x, y)

plt.title('Cases according to dates', fontsize = 12)
plt.xlabel('Dates', fontsize = 12)
plt.ylabel('Cases numbers', fontsize = 12)
plt.grid(True)

# print(df)

# df.info()

# df.shape 

# df.isnull().any()

# df['price']
