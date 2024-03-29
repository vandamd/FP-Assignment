#Elias


# Misc
import json
import requests
from datetime import date
import re
import plotly.io as pio
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)


polygons = requests.get(
    "https://gist.githubusercontent.com/duhaime/1d6d5a8dc77c86128fcc1a05a72726c9/raw/8b8522cbc69498b6c4983a9f58c045c2b451cb89/british-isles-counties.geojson"
).json()


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
    dcc.Graph(
        id='final-graph'
    ),

    # Output Choropleth Map with loading animation
    dcc.Loading(
        id="loading-1",
        children=[dcc.Graph(id="map-graph")],
        type="circle",
    )

])


# When City and dates selected, graph updates with specified values
@app.callback(
    Output('final-graph', 'figure'),
    Input('city-dropdown', 'value'),
    Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date')
)
def update_output(city, start_date, end_date):
    N = len(city)

    fig = make_subplots(
        rows=2, cols=2,
        shared_xaxes=True,
        vertical_spacing=0.03,
        column_widths=[1, 0.4],
        # row_heights=[0.2, 1],
        specs=[[{"secondary_y": True}, {"type": "pie"}],
               [{"type": "scatter"}, {"type": "choropleth"}]])

    for i in range(N):
        df_filtered = df[df['areaName'].str.contains(r'\b' + city[i] + r'\b')]
        df_reset = df_filtered.reset_index(drop=True)
        first_dose_people = df_reset.loc[0,
                                         'cumPeopleVaccinatedFirstDoseByVaccinationDate']
        second_dose_people = df_reset.loc[0,
                                          'cumPeopleVaccinatedSecondDoseByVaccinationDate']
        third_dose_people = df_reset.loc[0,
                                         'cumPeopleVaccinatedThirdInjectionByVaccinationDate']
        values = [first_dose_people, second_dose_people, third_dose_people]

        fig.add_trace(
            go.Scatter(
                x=df_filtered["date"],
                y=df_filtered['cumCasesBySpecimenDate'],
                mode="lines",
                name="Total Cases for " + str(city[i])
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df_filtered["date"],
                y=df_filtered['newCasesBySpecimenDate'],
                name="New Cases for " + str(city[i])),
            secondary_y=True,
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df_filtered["date"],
                y=df_filtered['cumPeopleVaccinatedFirstDoseByVaccinationDate'],
                mode="lines",
                name="First Dose for " + str(city[i])
            ),
            row=2, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df_filtered["date"],
                y=df_filtered['cumPeopleVaccinatedSecondDoseByVaccinationDate'],
                name="Second Dose for " + str(city[i])
            ),
            row=2, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df_filtered["date"],
                y=df_filtered['cumPeopleVaccinatedThirdInjectionByVaccinationDate'],
                name="Third Dose for " + str(city[i])
            ),
            row=2, col=1
        )
        colors = ['green', 'purple', 'orange']
        fig.add_trace(
            go.Pie(
                labels=['First Dose', 'Second Dose', 'Third Injection'],
                values=values,
                textinfo='label+percent',
                marker=dict(
                   colors=colors, line=dict(color='#000000', width=0.2)),
                pull=[0, 0, 0],
                name="Vaccine Doses"),
            row=1, col=2)
        

    fig.update_geos(fitbounds="locations")
    fig.update_yaxes(title_text="Cumulative COVID-19 Cases", row=1, col=1)
    fig.update_yaxes(title_text="New Cases", row=1, col=1, secondary_y=True)
    fig.update_yaxes(title_text="Vaccine Doses", row=2, col=1)

    fig.update_xaxes(title_text="", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_layout(xaxis_range=[start_date, end_date])
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
        ),
    )
    fig.update_xaxes(matches='x')
    fig.update_layout(title_text="COVID-19 Data")
    fig.update_layout(xaxis_range=[start_date, end_date])
    fig.update_layout(height=1000, autosize=True)

    return fig


# Ouput Choropleth graph - doesn't take any inputs currently
@app.callback(
    Output('map-graph', 'figure'),
    Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date')
)
def update_map(start_date, end_date):
    df = pd.read_csv(url)
    df["date2"] = pd.to_datetime(df['date'])
    df = df[df['date2'].dt.day == 1]

    fig1 = px.choropleth_mapbox(
        df.iloc[::-1],
        geojson=polygons,
        locations='areaName',
        featureidkey="properties.NAME_2",
        color='newCasesBySpecimenDate',
        color_continuous_scale="Reds",
        range_color=(0, 500),
        hover_name='areaName',
        labels={"newCasesBySpecimenDate": "Cases"},
        animation_frame="date",
        animation_group="areaCode",
        center={"lat": 54.768483, "lon": -4.417318},
        mapbox_style="carto-positron", zoom=5
    )

    fig1.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig1.update_geos(fitbounds="geojson", visible=False)
    fig1.update_layout(height=1000, autosize=True)
    # fig.show()
    return fig1


# Testing
if __name__ == '__main__':
    app.run_server(debug=True)

