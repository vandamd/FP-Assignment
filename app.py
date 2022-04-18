# Misc
from datetime import date
from dash import Dash, html, dcc, Input, Output
import pandas as pd

app = Dash(__name__)

# URL of CSV 
url = 'https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&metric=cumCasesBySpecimenDate&metric=cumPeopleVaccinatedFirstDoseByVaccinationDate&metric=cumPeopleVaccinatedSecondDoseByVaccinationDate&metric=newCasesBySpecimenDate&metric=cumPeopleVaccinatedThirdInjectionByVaccinationDate&format=csv'


# Read CSV
df = pd.read_csv(url)

# Determining the maximum date range - YYYY-MM-DD
dMin_value, dMax_value = df['date'].min(), df['date'].max()


# BUG WITH DASH PLOTLY - Cannot select cities with commas
# Renaming the cities with commas
df.replace(to_replace="Armagh City, Banbridge and Craigavon",
           value="Armagh City and Banbridge and Craigavon",
           inplace=True)
df.replace(to_replace="Bristol, City of",
           value="Bristol",
           inplace=True)
df.replace(to_replace="Bournemouth, Christchurch and Poole",
           value="Bournemouth and Christchurch and Poole",
           inplace=True)
df.replace(to_replace="Herefordshire, County of",
           value="Herefordshire",
           inplace=True)
df.replace(to_replace="Kingston upon Hull, City of",
           value="Kingston upon Hull",
           inplace=True)
df.replace(to_replace="Newry, Mourne and Down",
           value="Newry and Mourne and Down",
           inplace=True)


# City list
areaList = sorted(list(set(df['areaName'].tolist())))




########## Page Formatting
# Formatting style for City and Date Input
style_dict = dict(width='100%',
                  # border='1.5px black solid',
                  height='50px',
                  # textAlign='center',
                  fontFamily='HelveticaNeue',
                  fontSize=20)


# Formatting for Header and Description
style_dict1 = dict(
    # border='1.5px black solid',
    # height='50px',
    textAlign='center',
    fontFamily='HelveticaNeue',
)


# Layout
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
            ['Bristol'],
            id='city-dropdown',
            multi=True,
            style=style_dict,
        ),
        style={'width': '40%', 'display': 'flex', 'vertical-align': 'top',
               'margin-left': 'auto', 'margin-right': 'auto'}
    ),

    # Placeholder
    html.Div(style={'width': '2%', 'display': 'inline-block',
             'vertical-align': 'top'}),

    # Date Range Picker
    html.Div(
        dcc.DatePickerRange(
            id='date-range-picker',
            min_date_allowed=date(int(dMin_value[0:4]), int(
                dMin_value[5:7]), int(dMin_value[8:10])),
            max_date_allowed=date(int(dMax_value[0:4]), int(
                dMax_value[5:7]), int(dMax_value[8:10])),
            start_date=date(int(dMin_value[0:4]), int(
                dMin_value[5:7]), int(dMin_value[8:10])),
            end_date=date(int(dMax_value[0:4]), int(
                dMax_value[5:7]), int(dMax_value[8:10])),
            style=style_dict,
        ),
        style={'width': '40%', 'display': 'flex', 'vertical-align': 'top',
               'margin-left': 'auto', 'margin-right': 'auto'}
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
