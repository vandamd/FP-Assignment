# Misc
from datetime import date
from dash import Dash, html, dcc, Input, Output
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.express as px
import requests
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

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
            ['Bristol', 'Hackney and City of London'],
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
    ),
    
    # Output Choropleth Map with loading animation
    html.Div(
        dcc.Loading(
            id="loading-1",
            children=[dcc.Graph(id="map-graph")],
            type="circle",
        ),
        style = {'width': '40%', 'align-items': 'center', 'justify-content': 'center', 'margin-left': 'auto', 'margin-right': 'auto'}
    )
])

########## Data Inputs and Outputs
##### Main Graph
# When City and dates are selected, graph updates with specified values
@app.callback(
    Output('final-graph', 'figure'),
    Input('city-dropdown', 'value'),
    Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date')
)


def update_output(city, start_date, end_date):
    N = len(city)
    
    colorsTotalCases = ['#ff002b', '#0077b6']        #light     red-blue
    colorsNewCases =  ['#c00021', '#023e8a']         #dark      red-blue
    colorsVacc1 = ['#ff6000', '#004b23']             #dark      orange-green
    colorsVacc2 = ['#ff7900', '#38b000']             #mid       orange-green
    colorsVacc3 = ['#ffd000', '#9ef01a']             #light     orange-green
    colorsPie1 = ['#ff6000', '#ff7900', '#ffd000']   #orange    dark-light
    colorsPie2 = ['#004b23', '#38b000','#9ef01a']    #green     dark-light
    
    fig = make_subplots(
        rows=4, cols=2,
        shared_xaxes=True,
        vertical_spacing=0.08,
        column_widths=[1, 1],
        row_heights=[1, 1, 0.5, 1],
        subplot_titles=("COVID-19 Cases", "Vaccine Doses", "Vaccine Doses Percentage"),
        specs=[[{"secondary_y": True, "colspan": 2}, None],
               [{"type": "scatter", "colspan": 2}, None],
               [None, None],
               [{"type": "pie"}, {"type": "pie"}]])
    
    
    for i in range(N):
        df_filtered = df[df['areaName'].str.contains(r'\b' + city[i] + r'\b')]
        
            
        # Graph of Cumulative Cases against Time (1)
        fig.add_trace(
            go.Scatter(
                x=df_filtered["date"],
                y=df_filtered['cumCasesBySpecimenDate'],
                mode="lines",
                name="Total Cases for " + str(city[i]),
                line=dict(color=colorsTotalCases[i])
            ),
            row=1, col=1
        )
        
        # Graph of New Cases against Time - on top of (1)
        fig.add_trace(
            go.Scatter(
                x=df_filtered["date"],
                y=df_filtered['newCasesBySpecimenDate'],
                name="New Cases for " + str(city[i]),
                line=dict(color=colorsNewCases[i])),
            secondary_y=True,
            row=1, col=1
        )

        # Graph of First Vaccine Doses against Time
        fig.add_trace(
            go.Scatter(
                x=df_filtered["date"],
                y=df_filtered['cumPeopleVaccinatedFirstDoseByVaccinationDate'],
                mode="lines",
                name="First Dose for " + str(city[i]),
                line=dict(color=colorsVacc1[i])
            ),
            row=2, col=1
        )

        # Graph of Second Vaccine Doses against Time
        fig.add_trace(
            go.Scatter(
                x=df_filtered["date"],
                y=df_filtered['cumPeopleVaccinatedSecondDoseByVaccinationDate'],
                name="Second Dose for " + str(city[i]),
                line=dict(color=colorsVacc2[i])
            ),
            row=2, col=1
        )

        # Graph of Third Vaccine Doses against Time
        fig.add_trace(
            go.Scatter(
                x=df_filtered["date"],
                y=df_filtered['cumPeopleVaccinatedThirdInjectionByVaccinationDate'],
                name="Third Dose for " + str(city[i]),
                line=dict(color=colorsVacc3[i])
            ),
            row=2, col=1
        )
    
    # 1st Pie Chart Values   
        df_filtered = df[df['areaName'].str.contains(r'\b' + city[0] + r'\b')]
        df_reset = df_filtered.reset_index(drop=True)
        first_dose_people = df_reset.loc[0, 'cumPeopleVaccinatedFirstDoseByVaccinationDate']
        second_dose_people = df_reset.loc[0, 'cumPeopleVaccinatedSecondDoseByVaccinationDate']
        third_dose_people = df_reset.loc[0, 'cumPeopleVaccinatedThirdInjectionByVaccinationDate']
        values = [first_dose_people, second_dose_people, third_dose_people]
    
      # Pie Chart of Vaccine Doses
        
        fig.add_trace(
                  go.Pie(
                      labels=['First Dose', 'Second Dose', 'Third Injection'],
                      values=values,
                      textinfo='label+percent',
                      marker=dict(
                          colors=colorsPie1,line=dict(color='#000000', width=0.2)),
                      pull=[0, 0, 0],
                      name="Vaccine Doses",
                      showlegend = False),
                  row=4, col=1)
     # 2nd Pie Chart Value
        if N==2:   
            df_city2 = df[df['areaName'].str.contains(r'\b' + city[1] + r'\b')]
            df_reset2 = df_city2.reset_index(drop=True)
            first_dose_people2 = df_reset2.loc[0, 'cumPeopleVaccinatedFirstDoseByVaccinationDate']
            second_dose_people2 = df_reset2.loc[0, 'cumPeopleVaccinatedSecondDoseByVaccinationDate']
            third_dose_people2 = df_reset2.loc[0, 'cumPeopleVaccinatedThirdInjectionByVaccinationDate']
            values2 = [first_dose_people2, second_dose_people2, third_dose_people2]
            fig.add_trace(
                go.Pie(
                    labels=['First Dose', 'Second Dose', 'Third Injection'],
                    values=values2,
                    textinfo='label+percent',
                    marker=dict(
                        colors=colorsPie2,line=dict(color='#000000', width=0.2)),
                    pull=[0, 0, 0],
                    name="Vaccine Doses",
                    showlegend = False),
                row=4, col=2)


    # Figure Formatting
    fig.update_yaxes(title_text="Cumulative COVID-19 Cases", row=1, col=1)     # Title of Left Y-Axis of Cases Graph
    fig.update_yaxes(title_text="New Cases", row=1, col=1, secondary_y=True)   # Title of Right Y-Axis of Cases Graph
    fig.update_yaxes(title_text="Vaccine Doses", row=2, col=1)                 # Title of Y-Axis of Vaccine Graph
    fig.update_xaxes(title_text="Date", row=2, col=1)                          # Title of X-Axis of Vaccine Graphs
    fig.update_xaxes(matches='x')                                              # Allows Cases and Vaccine Graph to zoom together
    fig.update_layout(height=1000, autosize=True)                              # Height of the Final Graph
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
             
    return fig                                                                 # Show Graph!


##### Choropleth Graph
# Geojson File
polygons_path = 'Counties_and_Unitary_Authorities_(December_2021)_UK_BUC.geojson'
with open(polygons_path) as p:
    polygons = json.load(p)

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
        locations='areaCode',
        featureidkey="properties.CTYUA21CD",
        color='newCasesBySpecimenDate',
        color_continuous_scale="Reds",
        range_color=(0, 2000),
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




if __name__ == '__main__':
    app.run_server(debug=True)
