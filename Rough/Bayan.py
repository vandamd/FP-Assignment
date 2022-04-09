
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

# New Cases, Cumulative Cases & Vaccines
url3 = 'https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&metric=cumCasesBySpecimenDate&metric=cumPeopleVaccinatedFirstDoseByVaccinationDate&metric=cumPeopleVaccinatedSecondDoseByVaccinationDate&metric=newCasesBySpecimenDate&metric=cumPeopleVaccinatedThirdInjectionByVaccinationDate&format=csv'





##### FUNCTIONS #####
def UserChoice():
    """
      * The initial startup question for the user. 
      - Sets a variable called 'error' as false. 
      - While 'error' is not 'false', i.e. while 'error' is true, the input 
        question will repeat until a correct input is entered.
      - When the choice 'c' is entered, 'error' becomes 'true', thus stops
        the while loop.
      - When the choice 'l' is entered, 'error' stays 'false', and the 
        ShowList() function is called to show the user the list of locations.
        UserChoice() is then repeated to allow the user to choose what to do
        next.
      - When the choice 'q' is entered, the loop is broken thus stopping the
        program.
    """
    global choice
    
    error = False
    while not error:
        choice = input(
            '\nPlease choose what to do:\n  l: Show list of cities\n  c: '
            'Choose cities\n  q: Quit\n\n» Action: ')
        if choice in ['c']:
            error = choice in ['c']
        elif choice in ['l']:
            ShowList()
        elif choice in ['q']:
            break
        else:
            print("\nOops! Didn't quite catch that!")




def ShowList():
    """
      * Shows the list of locations.
      - Currently reads all the data in the areaName column of the csv file.
      - Converts the column into a list.
      - Then converts the list into a set to remove duplicates.
      - Each of the elements of the set are then seperated with line breaks
        and outputted for the user to see.
    """
    df = pd.read_csv(url3)
    areaList = df['areaName'].tolist()
    areaSet = set(areaList)
    areaList = list(areaSet)
    areaList = sorted(areaList)
    print()
    print(*areaList, sep='\n')




def LocationInput():
    """
      * Asks the user to input a location or multiple locations.
      - Removes the spaces after each comma.
      - Splits cities that have commas in between them.
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
    # userLocations = userLocations.replace(" ", "|")
    
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
def graphgen():
            """
              - Determines the number of cities entered
              - If there is one city entered, generates a graph of covid cases
              - If there is more than one city entered, poop is outputted
            """
            # The number of words in userLocations
            #N = len(userLocationsList)
            
            # Instance for 1 Location inputted
            #if N == 1:
            
            global userLocationsList
        
            for location in userLocationsList:
                
                if location == userLocationsList[-1]:
                    break 
                '''
            - loops through every location in the list
            - supposed to break the loop when it reaches the last location
            '''
                
                for index in range(len(userLocationsList)):
                    if index == len(userLocationsList):
                        break
                    ''''
                    - iterates through the indices of locations in the list to use in df_filtered (userLocationsList[index])
                    - supposed to break when it reaches the last location 
                    '''
                    
                    
                    df = pd.read_csv(url3)
                    df_filtered = df[df['areaName'].str.contains(r'\b' + userLocationsList[index] + r'\b')]
                    df_reset = df_filtered.reset_index(drop=True)
                    
                    
                    first_dose_people = df_reset.loc[index,'cumPeopleVaccinatedFirstDoseByVaccinationDate']
                    second_dose_people = df_reset.loc[index,'cumPeopleVaccinatedSecondDoseByVaccinationDate']
                    third_dose_people = df_reset.loc[index,'cumPeopleVaccinatedThirdInjectionByVaccinationDate']
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
                               [{"type": "scatter"}, {"type": "choropleth"}]])
                    
                    fig.add_trace(
                        go.Scatter(
                            x=df_filtered["date"],
                            y=df_filtered['cumCasesBySpecimenDate'],
                            mode="lines",
                            name="COVID-19 Cases",
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
                    
                    
                    
                    
                    fig.add_trace(          # GEOGRAPHICAL MAP
                        go.Choropleth(
                            geojson = '/Users/vandam/Library/Mobile Documents/com~apple~CloudDocs/Documents/School/Year 1/Programming/Documents/Further Programming/FP-Assignment/Rough/lad.json',
                            locationmode = 'geojson-id',
                            # featureidkey='properties.LAD13NM',
                            # locations=df_filtered["areaName"],
                            # color=df_filtered["cumCasesBySpecimenDate"],
                            # color_continuous_scale='Reds',
                            # locationmode = 'geojson-id',
                            # color='cumCasesBySpecimenDate',
                            # color=df_filtered['cumCasesBySpecimenDate'],
                            # hover_name=df_filtered["areaName"],
                            # animation_frame=df_filtered["date"],
                            name="COVID-19 Cases",
                        ),
                        row=2, col=2
                    )
                    
                    
                    
                    
                    
                    
                    
                    fig.update_yaxes(title_text="Cumulative COVID-19 Cases", row=1, col=1)
                    fig.update_yaxes(title_text="New Cases", row=1, col=1, secondary_y=True)
                    fig.update_yaxes(title_text="Vaccine Doses", row=2, col=1)
                    
                    fig.update_xaxes(title_text="", row=1, col=1)
                    fig.update_xaxes(title_text="Date", row=2, col=1)
                    
                    fig.update_layout(title_text="COVID-19 Data")
                    fig.update_layout(xaxis_range=[start_date, end_date])
                    # fig.update_geos(scope='europe') 
                    
                    fig.update_layout(
                        xaxis=dict(
                            rangeselector=dict(
                                buttons=list(
                                    [
                                        dict(count=1, label="1m", step="month", stepmode="backward"),
                                        dict(count=6, label="6m", step="month", stepmode="backward"),
                                        dict(count=1, label="1y", step="year", stepmode="backward"),
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
                    
                        
                    #elif N > 1:
                        #print('poop')
            












##### TEST AREA #####
UserChoice()




if choice == 'l':
    ShowList()
if choice == 'c':
    LocationInput()
    timeRange()
    graphgen()


        