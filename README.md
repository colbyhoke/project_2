# project_2

## Files overview
* Everything in /heroku is what we have in production on: https://secure-river-49709.herokuapp.com
* The files in /setup are what you would use to ETL the data. That includes a Jupyter Notebook and a .sql file used to query and set up the Postgres database.
* /static holds the CSS, Javascript, and favicon files
* /templates holds all of the html files that get served by app.py in the home folder
* app.py is the Flask application to run the dashboard locally
* state_abbrev.py is an adapted GitHub project to look up / match state names with abbreviations. This helps the API routing translate input to match with database entries.

## Our project proposal:
### Overview:
We're going to revisit some of the COVID data that had been used previously in the class, specifically the New York Times daily data.
We plan to map all of this data out using Leaflet / Mapbox.
We're also going to combine this data with CDC data that documents excess deaths in the US to build a visual representation of what these cases and deaths look like over time and how that compares to expected deaths.



### Data sources:
* NYTimes COVID data: https://github.com/nytimes/covid-19-data
* CDC: Excess Deaths Associated with COVID-19: https://www.cdc.gov/nchs/nvss/vsrr/covid19/excess_deaths.htm




### Visual inspiration:



## Project requirements:
1. Your visualization must include a Python Flask–powered RESTful API, HTML/CSS, JavaScript, and at least one database (SQL, MongoDB, SQLite, etc.).
2. Your project should fall into one of the below four tracks:
    - A custom “creative” D3.js project (i.e., a nonstandard graph or chart)
    - A combination of web scraping and Leaflet or Plotly
    - A dashboard page with multiple charts that update from the same data
   - A “thick” server that performs multiple manipulations on data in a database prior to visualization (must be approved)
3. Your project should include at least one JS library that we did not cover.
4. Your project must be powered by a data set with at least 100 records.
5. Your project must include some level of user-driven interaction (e.g., menus, dropdowns, textboxes).
6. Your final visualization should ideally include at least three views.



