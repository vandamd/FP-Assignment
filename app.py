# Misc
from datetime import date
from dash import Dash, html, dcc, Input, Output
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objs as go

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
    ),
    
    # Output Main Graph
    html.Div(
        dcc.Graph(
            id='final-graph'
        ),
        style = {'width': '70%', 'align-items': 'center', 'justify-content': 'center', 'margin-left': 'auto', 'margin-right': 'auto'}
    )
])

########## Data Inputs and Outputs
# When City and dates are selected, graph updates with specified values
@app.callback(
    Output('final-graph', 'figure'),
    Input('city-dropdown', 'value'),
    Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date')
)
def update_output(city, start_date, end_date):
    N = len(city)
    
    fig = make_subplots(
        rows=4, cols=2,
        shared_xaxes=True,
        vertical_spacing=0.03,
        column_widths=[1, 1],
        row_heights=[1, 1, 1, 1],
        specs=[[{"secondary_y": True, "colspan": 2}, None],
               [{"type": "scatter", "colspan": 2}, None],
               [None, None],
               [None, None]])

    for i in range(N):
        df_filtered = df[df['areaName'].str.contains(r'\b' + city[i] + r'\b')]

        # Graph of Cumulative Cases against Time (1)
        fig.add_trace(
            go.Scatter(
                x=df_filtered["date"],
                y=df_filtered['cumCasesBySpecimenDate'],
                mode="lines",
                name="Total Cases for " + str(city[i])
            ),
            row=1, col=1
        )
        
        # Graph of New Cases against Time - on top of (1)
        fig.add_trace(
            go.Scatter(
                x=df_filtered["date"],
                y=df_filtered['newCasesBySpecimenDate'],
                name="New Cases for " + str(city[i])),
            secondary_y=True,
            row=1, col=1
        )

        # Graph of First Vaccine Doses against Time
        fig.add_trace(
            go.Scatter(
                x=df_filtered["date"],
                y=df_filtered['cumPeopleVaccinatedFirstDoseByVaccinationDate'],
                mode="lines",
                name="First Dose for " + str(city[i])
            ),
            row=2, col=1
        )

        # Graph of Second Vaccine Doses against Time
        fig.add_trace(
            go.Scatter(
                x=df_filtered["date"],
                y=df_filtered['cumPeopleVaccinatedSecondDoseByVaccinationDate'],
                name="Second Dose for " + str(city[i])
            ),
            row=2, col=1
        )

        # Graph of Third Vaccine Doses against Time
        fig.add_trace(
            go.Scatter(
                x=df_filtered["date"],
                y=df_filtered['cumPeopleVaccinatedThirdInjectionByVaccinationDate'],
                name="Third Dose for " + str(city[i])
            ),
            row=2, col=1
        )

    # Figure Formatting
    fig.update_yaxes(title_text="Cumulative COVID-19 Cases", row=1, col=1)     # Title of Left Y-Axis of Cases Graph
    fig.update_yaxes(title_text="New Cases", row=1, col=1, secondary_y=True)   # Title of Right Y-Axis of Cases Graph
    fig.update_yaxes(title_text="Vaccine Doses", row=2, col=1)                 # Title of Y-Axis of Vaccine Graph
    fig.update_xaxes(title_text="Date", row=2, col=1)                          # Title of X-Axis of Vaccine Graphs
    fig.update_xaxes(matches='x')                                              # Allows Cases and Vaccine Graph to zoom together
    fig.update_layout(height=1000, autosize=True)                              # Height of the Final Graph
    fig.update_layout(xaxis_range=[start_date, end_date])                      # Update Date using Date Range Picker
    
    return fig                                                                 # Show Graph!







if __name__ == '__main__':
    app.run_server(debug=True)
