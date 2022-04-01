"""
Made with love by,

Vandam :)
"""

##### PACKAGES #####

import re
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objs as go
from plotly.subplots import make_subplots
pio.renderers.default = 'browser'           # Displays the graph in the Browser


##### URLS #####

# Spreadsheet for all COVID-19 Cases and Vaccine Doses for all areas in the UK
url = 'https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&metric=cumCasesBySpecimenDate&metric=cumPeopleVaccinatedFirstDoseByVaccinationDate&metric=cumPeopleVaccinatedSecondDoseByVaccinationDate&metric=cumPeopleVaccinatedThirdInjectionByVaccinationDate&format=csv'
url2 = 'https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&metric=cumPeopleVaccinatedFirstDoseByVaccinationDate&metric=cumPeopleVaccinatedSecondDoseByVaccinationDate&metric=cumPeopleVaccinatedThirdInjectionByVaccinationDate&metric=newCasesBySpecimenDate&metric=cumCasesBySpecimenDate&format=csv'

# New Cases, Cumulative Cases, Vaccines
url3 = 'https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&metric=cumCasesBySpecimenDate&metric=cumPeopleVaccinatedFirstDoseByVaccinationDate&metric=cumPeopleVaccinatedSecondDoseByVaccinationDate&metric=newCasesBySpecimenDate&metric=cumPeopleVaccinatedThirdInjectionByVaccinationDate&format=csv'





##### FUNCTIONS #####
def UserChoice():                                    # Initial startup question
    global choice
    choice = input(
        '\nPlease choose what to do:\n  l: Show list of cities\n  c: '
        'Choose cities\n  q: Quit\n\n» Action: ')




def ShowList():
    """
      - Shows the list of locations
      - Currently reads all the data in the areaName column of the csv file.
      - Sorts into a list, then prints a set to remove duplicates
    """
    df = pd.read_csv(url)
    areaList = df['areaName'].tolist()
    print(set(areaList))
    restart = input('\nTo continue press enter: ')
    if restart == '':
        UserChoice()




def LocationInput():
    """
      - Asks the user to input a location or multiple locations.
      - Removes the spaces after each comma.
      - Replaces the spaces between the words of two worded cities with |.
        This allows us to find the exact match of the city later in the
        graph gen function, instead of matching with other cities. This is 
        common for cities that contain with 'North', 'South', 'East', 'West'
        and 'and'.
    """
    global userLocationsList
    userLocations = input(
        "Please enter the location(s) you would like data for:\n  You can "
        "enter a single location, or multiple locations seperated with commas."
        "\n\n  Examples:\n  Bristol - Only data for Bristol will be shown.\n  "
        "Liverpool, London - Data for both Liverpool and London will be shown."
        "\n\n» Location(s): ")
    
    # Removes the spaces after the commas
    userLocations = userLocations.replace(", ", ",")
    # Replaces the spaces between two-worded cities with |
    userLocations = userLocations.replace(" ", "|")
    # Splits cities into a list, where the user seperates the cities with commas
    userLocationsList = userLocations.split(",")




def timeRange():
    global start_date
    global end_date
    
    df = pd.read_csv(url3)
    df_filtered = df[df['areaName'].str.contains(r'\b' + userLocationsList[0] + r'\b')]
    min_value, max_value = df_filtered['date'].min(), df_filtered['date'].max()
    
    print('\nPlease select a time range:\n  Possible start date:', min_value, 
          '\n  Possible end date:', max_value, '\n\n  Examples:\n  All - '
          'this will display data across the whole time range.\n  YYYY-MM-DD'
          ' - YYYY-MM-DD - This will display data for the specified dates.')
    DateInput = input("» Time Range: ")
    
    if DateInput == "All":
        start_date = min_value
        end_date = max_value
    elif DateInput != "All":
        DateInput = DateInput.replace(' - ', ',')
        # DateInput = DateInput.replace('/', '-')
        DateInput = DateInput.split(",")
        start_date = DateInput[0]
        end_date = DateInput[1]
        
    # print(start_date, end_date)



# Generates Graph
def graphgen(userLocationsList):
    """
      - Determines the number of cities entered
      - If there is one city entered, generates a graph of covid cases
      - If there is more than one city entered, poop is outputted
    """
    # The number of words in userLocations
    N = len(userLocationsList)
    
    # Instance for 1 Location inputted
    if N == 1:
        df = pd.read_csv(url3)
        df_filtered = df[df['areaName'].str.contains(r'\b' + userLocationsList[0] + r'\b')]
        df_reset = df_filtered.reset_index(drop=True)
        
        
        first_dose_people = df_reset.loc[0,'cumPeopleVaccinatedFirstDoseByVaccinationDate']
        second_dose_people = df_reset.loc[0,'cumPeopleVaccinatedSecondDoseByVaccinationDate']
        third_dose_people = df_reset.loc[0,'cumPeopleVaccinatedThirdInjectionByVaccinationDate']
        values = [first_dose_people, second_dose_people, third_dose_people]
        
        
        
        ### ACTUAL GRAPH GEN PART ###
        
        
        # Subplots
        fig = make_subplots(
            rows=2, cols=2,
            shared_xaxes=True,
            vertical_spacing=0.03,
            column_widths=[1, 0.4],
            # row_heights=[0.2, 1],
            specs=[[{"secondary_y": True}, {"type": "pie"}],
                   [{"type": "scatter"}, None]])
        
        fig.add_trace(
            go.Scatter(
                x=df_filtered["date"],
                y=df_filtered['cumCasesBySpecimenDate'],
                mode="lines",
                name="COVID-19 Cases"
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df_filtered["date"], 
                y=df_filtered['newCasesBySpecimenDate'], 
                name="New COVID-19 Cases"),
            secondary_y=True,
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df_filtered["date"],
                y=df_filtered['cumPeopleVaccinatedFirstDoseByVaccinationDate'],
                mode="lines",
                name="First Dose"
            ),
            row=2, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df_filtered["date"], 
                y=df_filtered['cumPeopleVaccinatedSecondDoseByVaccinationDate'], 
                name="Second Dose"),
            row=2, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df_filtered["date"], 
                y=df_filtered['cumPeopleVaccinatedThirdInjectionByVaccinationDate'], 
                name="Third Dose"),
            row=2, col=1
        )

        fig.add_trace(
            go.Pie(
                labels=['First Dose','Second Dose', 'Third Injection'], 
                values=values, 
                textinfo='label+percent', 
                pull=[0,0,0],
                name="Vaccine Doses"
            ), 
            row=1, col=2
        )
        
        fig.update_yaxes(title_text="Cumulative COVID-19 Cases", row=1, col=1)
        fig.update_yaxes(title_text="New Cases", row=1, col=1, secondary_y=True)
        fig.update_yaxes(title_text="Vaccine Doses", row=2, col=1)
        
        fig.update_xaxes(title_text="", row=1, col=1)
        fig.update_xaxes(title_text="Date", row=2, col=1)
        
        fig.update_layout(title_text="COVID-19 Data")
        fig.update_layout(xaxis_range=[start_date, end_date])
        fig.show()
        
        
        # # Line Chart
        # fig1 = px.line(df_filtered, x = 'date', 
        #                y = ['cumCasesBySpecimenDate',
        #                     'cumPeopleVaccinatedFirstDoseByVaccinationDate', 
        #                     'cumPeopleVaccinatedSecondDoseByVaccinationDate',
        #                     'cumPeopleVaccinatedThirdInjectionByVaccinationDate'], 
        #                labels=dict(x="Date", y="Number of people"))
        # fig1.update_layout(xaxis_range=[start_date, end_date])
        # fig1.show()
        
        # # Pie Chart
        # first_dose_people = df_reset.loc[0,'cumPeopleVaccinatedFirstDoseByVaccinationDate']
        # second_dose_people = df_reset.loc[0,'cumPeopleVaccinatedSecondDoseByVaccinationDate']
        # third_dose_people = df_reset.loc[0,'cumPeopleVaccinatedThirdInjectionByVaccinationDate']
        # values = [first_dose_people, second_dose_people, third_dose_people]
                
        # fig2 = go.Figure(data=[go.Pie(labels=['First Dose','Second Dose', 'Third Injection'], values=values, textinfo='label+percent', pull=[0.1,0.1,0.1])])
        # fig2.show()
        
        
    elif N > 1:
        print('poop')








##### TEST AREA #####
UserChoice()
if choice == 'l':
    ShowList()
if choice == 'c':
    LocationInput()
    timeRange()
    graphgen(userLocationsList)

