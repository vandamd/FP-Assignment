

import pandas as pd
import plotly.express as px
import plotly.io as pio
            

pio.renderers.default = 'browser'           # Displays the graph in the Browser





# Reads the URL of the CSV file
df = pd.read_csv('https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&areaCode=E06000023&metric=cumPeopleVaccinatedFirstDoseByVaccinationDate&metric=cumPeopleVaccinatedSecondDoseByVaccinationDate&metric=cumPeopleVaccinatedThirdInjectionByVaccinationDate&metric=cumCasesByPublishDate&format=csv')


#allow user to choose a time range
start_date = input('Input desired start date as follows(YYYY-MM-DD):' )
end_date = input('Input desired end date as follows(YYYY-MM-DD):' )


    
# Show fig, x axis, y axis 
fig = px.line(df, x = 'date', y = ['cumCasesByPublishDate','cumPeopleVaccinatedFirstDoseByVaccinationDate','cumPeopleVaccinatedSecondDoseByVaccinationDate','cumPeopleVaccinatedThirdInjectionByVaccinationDate'])
fig.update_layout(xaxis_range=[start_date,end_date])     #sets range selected for date axis
fig.show()


min_value = df['date'].min()
        max_value = df['date'].max()
        print('Select a time range between', min_value, 'and', max_value)
        start_date = input('Input desired start date as follows(YYYY-MM-DD):' )
        end_date = input('Input desired end date as follows(YYYY-MM-DD):' )