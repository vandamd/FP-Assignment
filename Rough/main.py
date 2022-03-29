
##### PACKAGES #####

import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'browser'           # Displays the graph in the Browser


##### URLS #####

# Spreadsheet for all COVID-19 Cases and Vaccine Doses for all areas in the UK
url = 'https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&metric=cumCasesBySpecimenDate&metric=cumPeopleVaccinatedFirstDoseByVaccinationDate&metric=cumPeopleVaccinatedSecondDoseByVaccinationDate&metric=cumPeopleVaccinatedThirdInjectionByVaccinationDate&format=csv'


##### FUNCTIONS #####
def UserChoice():     # Initial startup question
    global choice
    choice = input(
        '\nPlease choose what to do: \n  l: Show list of locations\n  q: Quit\n\n» Action: ')

def UserChoice2():     #selection after seeing the list
    global choice
    choice = input(
        '\nPlease choose what to do next: \n  c: '
        'Choose a location\n  q: Quit\n\n» Action: ')







# Shows list of locations
def ShowList():                                       # Shows list of locations
    df = pd.read_csv(url)
    areaList = df['areaName'].tolist()
    print(set(areaList))
    len(set(areaList))
    




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

    # The number of words in userLocations
    N = len(userLocationsList)
    
    # Instance for 1 Location inputted
    if N == 1:
        df = pd.read_csv(url)
        df_filtered = df[df['areaName'].str.contains(r'\b' + userLocationsList[0] + r'\b')]
        # print(df_filtered)
        df_new = df_filtered.reset_index(drop=True)
        
        
        min_value = df['date'].min()
        max_value = df['date'].max()
        print('Select a time range between', min_value, 'and', max_value)
        start_date = input('Input desired start date as follows(YYYY-MM-DD):' )
        end_date = input('Input desired end date as follows(YYYY-MM-DD):' )
        #df_filtered.get_value([0], 'date')
        ### ACTUAL GRAPH GEN PART ###
        fig = px.line(df_filtered, x ='date', y = ['cumCasesBySpecimenDate','cumPeopleVaccinatedFirstDoseByVaccinationDate','cumPeopleVaccinatedSecondDoseByVaccinationDate','cumPeopleVaccinatedThirdInjectionByVaccinationDate'], title='Covid Rates')
        fig.show()
        
        
        date = df_new.loc[0,'date']
        
        first_dose_people = df_new.loc[0,'cumPeopleVaccinatedFirstDoseByVaccinationDate']
        
        second_dose_people = df_new.loc[0,'cumPeopleVaccinatedSecondDoseByVaccinationDate']
        
        third_dose_people = df_new.loc[0,'cumPeopleVaccinatedThirdInjectionByVaccinationDate']
        
        values = [first_dose_people, second_dose_people, third_dose_people]
                
        fig1 = px.pie(names=['First Dose','Second Dose', 'Third Injection'], values=values)
        
        fig1.show()
        
    elif N > 1:
        print('poop')








##### TEST AREA #####

UserChoice()
if choice == 'l':
    ShowList()
    UserChoice2()
    if choice == 'c':
        LocationInput()
        graphgen(userLocationsList)

