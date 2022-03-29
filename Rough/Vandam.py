"""
Made with love by,

Vandam :)
"""

##### PACKAGES #####

import re
import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'browser'           # Displays the graph in the Browser


##### URLS #####

# Spreadsheet for all COVID-19 Cases and Vaccine Doses for all areas in the UK
url = 'https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&metric=cumCasesBySpecimenDate&metric=cumPeopleVaccinatedFirstDoseByVaccinationDate&metric=cumPeopleVaccinatedSecondDoseByVaccinationDate&metric=cumPeopleVaccinatedThirdInjectionByVaccinationDate&format=csv'
url2 = 'https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&metric=cumPeopleVaccinatedFirstDoseByVaccinationDate&metric=cumPeopleVaccinatedSecondDoseByVaccinationDate&metric=cumPeopleVaccinatedThirdInjectionByVaccinationDate&metric=newCasesBySpecimenDate&metric=cumCasesBySpecimenDate&format=csv'

##### FUNCTIONS #####
def UserChoice():                                    # Initial startup question
    global choice
    choice = input(
        '\nPlease choose what to do:\n  l: Show list of locations\n  c: '
        'Choose locations\n  q: Quit\n\n» Action: ')





def ShowList():                                       # Shows list of locations
    """
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
        df = pd.read_csv(url2)
        df_filtered = df[df['areaName'].str.contains(r'\b' + userLocationsList[0] + r'\b')]
        ### ACTUAL GRAPH GEN PART ###
        #fig = px.line(df_filtered, x = 'date', y = ['newCasesBySpecimenDate','cumPeopleVaccinatedFirstDoseByVaccinationDate','cumPeopleVaccinatedSecondDoseByVaccinationDate','cumPeopleVaccinatedThirdInjectionByVaccinationDate'])
        fig = px.line(df_filtered, x = 'date', y = ['newCasesBySpecimenDate', 'cumCasesBySpecimenDate'])
        #fig.update_layout(xaxis_range=[start_date,end_date])
        fig.show()
    elif N > 1:
        print('poop')








##### TEST AREA #####
UserChoice()
if choice == 'l':
    ShowList()
if choice == 'c':
    LocationInput()
    graphgen(userLocationsList)