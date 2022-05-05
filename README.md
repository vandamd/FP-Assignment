# Further Computer Programming Assignment

A web application that displays COVID-19 data of cities across the United Kingdom. This uses data from <a href="https://coronavirus.data.gov.uk/">gov.uk</a> and is built with <a href="https://plotly.com/dash/">Dash Plotly</a>.


## Usage

The app can be viewed here on <a href="https://covid-19-uk.herokuapp.com/">Heroku</a> without the need to download anything. Suppose you want to host it locally, steps are provided below.


## Installation - (Packages are needed to run the functions on the Jupyter Notebook)

Clone the repository
```sh
git clone https://github.com/vandamd/FP-Assignment.git
```

Install Packages

- For Pip Users

  ```ssh
  pip install -r requirements.txt
  ```

- For Anaconda Users

  ```ssh
  conda install -c conda-forge dash
  conda install -c plotly plotly
  conda install -c anaconda pandas requests
  ```

Run the web application locally:
```ssh
cd FP-Assignment
python app.py
```

A link will be shown in your terminal, visit it in your browser.


## Notes

- A maximum of **two** cities can be selected.
- The graphs for the number of cases and vaccines share the same x-axis; drag and select a portion of the graph to zoom in or use the range slider found at the bottom of the graph. 
- To un-zoom, double click anywhere on the graph.
- The Pie Charts are independent from the date range picker. The most recent data entries for vaccine doses will be used.
- The Choropleth Graph is completely independent from user inputs.

#### Contributors
- vandamd - Vandam Dinh
- cloud-26/bwahib29 - Bayan Wahib
- maree26 - Margherita Parimbelli
- Github-Elias - Elias Momann 
