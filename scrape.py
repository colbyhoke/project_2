import pandas as pd
from sqlalchemy import create_engine
import json
import requests
from config import db_login_info

"""
NYT covid data
"""
# Pull in the live data
counties_path = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"

# Save to a dataframe
covid_all_df = pd.read_csv(counties_path)

# Drop rows with null values (we want complete data only)
covid_all_df = covid_all_df.dropna()

# Convert fips to int
covid_all_df = covid_all_df.astype({'fips': 'int'})

# Get the most up-to-date data
latest_date = covid_all_df['date'].iloc[-1]

# Make a dataframe holding that most recent data
covid_latest_df = covid_all_df.loc[covid_all_df['date']==latest_date]


"""
NYT mask data
"""
# Import the mask CSV data
mask_path = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/mask-use/mask-use-by-county.csv"
masks_df = pd.read_csv(mask_path)

# Clean up column names
masks_df.columns = ['fips','never','rarely','sometimes','frequently','always']

# Change the null values (no data) to 0
masks_df = masks_df.fillna(0)

"""
CDC data
"""
cdc_url = 'https://data.cdc.gov/resource/muzy-jte6.json'
response = requests.get(cdc_url)
cdc_json = response.json()

# Convert to a dataframe
cdc_df = pd.DataFrame.from_dict(cdc_json)

# Drop columns we don't need
cdc_df.drop(list(cdc_df)[19:34], axis=1,inplace=True)

# Rename columns
cdc_df.columns = ['state',
                  'year',
                  'week',
                  'week_ending_date',
                  'all_causes',
                  'natural_causes',
                  'septicemia',
                  'malignant_neoplasms',
                  'diabetes',
                  'alzheimers',
                  'influenza_and_pneumonia',
                  'chronic_lower_respiratory',
                  'other_diseases_of_respiratory',
                  'nephritis_nephrotic_syndrome',
                  'symptoms_signs_and_abnormal',
                  'diseases_of_heart',
                  'cerebrovascular_diseases',
                  'covid_19_multiple_causes',
                  'covid_19_underlying_cause']     


# Change the null values (no data) to 0
cdc_df = cdc_df.fillna(0)

# Build 2019 and 2020 dataframes, just in case
cdc_2019_df = cdc_df.loc[cdc_df['year']=="2019"]
cdc_2020_df = cdc_df.loc[cdc_df['year']=="2020"]


"""
Covid Tracking Project data
"""
covidtracking_current_url = 'https://api.covidtracking.com/v1/states/current.json'
covidtracking_current_response = requests.get(covidtracking_current_url)
covidtracking_current_json = covidtracking_current_response.json()

# Convert to a dataframe
covidtracking_current_df = pd.DataFrame.from_dict(covidtracking_current_json)

# Change the null values (no data) to 0
covidtracking_current_df = covidtracking_current_df.fillna(0)

# Remove columns we don't need
covidtracking_current_df.drop(list(covidtracking_current_df)[48:55], axis=1,inplace=True)
covidtracking_current_df.drop(list(covidtracking_current_df)[39], axis=1,inplace=True)
covidtracking_current_df.drop(list(covidtracking_current_df)[20], axis=1,inplace=True)
covidtracking_current_df.drop(list(covidtracking_current_df)[15:18], axis=1,inplace=True)

covidtracking_current_df.columns = ['date', 'state', 'positive', 'probable_cases', 'negative', 'pending',
       'total_test_results', 'hospitalized_currently', 'hospitalized_cumulative',
       'icu_currently', 'icu_cumulative', 'ventilator_currently',
       'ventilator_cumulative', 'recovered', 'data_quality_grade', 'deaths',
       'hospitalized', 'total_tests_viral', 'positive_tests_viral',
       'negative_tests_viral', 'positive_cases_viral', 'deaths_confirmed',
       'deaths_probable', 'total_test_encounters_viral', 'total_tests_people_viral',
       'total_tests_antibody', 'positive_tests_antibody', 'negative_tests_antibody',
       'total_tests_people_antibody', 'positive_tests_people_antibody',
       'negative_tests_people_antibody', 'total_tests_people_antigen',
       'positive_tests_people_antigen', 'total_tests_antigen',
       'positive_tests_antigen', 'positive_increase', 'negative_increase', 'total',
       'total_test_results_source', 'total_test_results_increase', 'pos_neg',
       'death_increase', 'hospitalized_increase']

covidtracking_all_url = 'https://api.covidtracking.com/v1/us/daily.json'
covidtracking_all_response = requests.get(covidtracking_all_url)
covidtracking_all_json = covidtracking_all_response.json()

# Convert to a dataframe
covidtracking_all_df = pd.DataFrame.from_dict(covidtracking_all_json)

# Change the null values (no data) to 0
covidtracking_all_df = covidtracking_all_df.fillna(0)

# Remove columns we don't need
covidtracking_all_df.drop(list(covidtracking_all_df)[24], axis=1,inplace=True)
covidtracking_all_df.drop(list(covidtracking_all_df)[16], axis=1,inplace=True)
covidtracking_all_df.drop(list(covidtracking_all_df)[12], axis=1,inplace=True)

covidtracking_all_df.columns = ['date', 'states', 'positive', 'negative', 'pending',
       'hospitalized_currently', 'hospitalized_cumulative', 'icu_currently',
       'icu_cumulative', 'ventilator_currently', 'ventilator_cumulative',
       'recovered', 'deaths', 'hospitalized', 'total_test_results', 'total',
       'pos_neg', 'death_increase', 'hospitalized_increase', 'negative_increase',
       'positive_increase', 'total_test_results_increase']

"""
County data
"""
# Scrape the county info table from Wikipedia
county_url = 'https://en.wikipedia.org/wiki/User:Michael_J/County_table'
county_table = pd.read_html(county_url)

# Grab the first table on the page and convert to dataframe
county_table_df = county_table[0]

# Drop columns we don't need
county_table_df = county_table_df.drop(columns=['Land Areakm²','Land Areami²','Water Areakm²','Water Areami²','Total Areakm²','Total Areami²','Sort [1]','Population(2010)'])

# Rename the columns
county_table_df.columns = ['state','fips','county','county_seat','lat','lon']

# Remove the + sign from latitude column
county_table_df['lat'] = county_table_df['lat'].str[1:]
county_table_df['lon'] = county_table_df['lon'].str[1:]

# Remove degree symbol from lat and lon
county_table_df['lat'] = county_table_df['lat'].str[:-1]
county_table_df['lon'] = county_table_df['lon'].str[:-1]

# Set as a float for lat and lon
county_table_df['lat'] = county_table_df['lat'].astype(float)
county_table_df['lon'] = county_table_df['lon'].astype(float)

# Convert the lon to an actual negative value (for all, since North America)
county_table_df['lon'] = -county_table_df['lon']

# Change the null values (no data) to 0
county_table_df = county_table_df.fillna(0)

"""
Connect to database
Note: db_login_info comes from config.py and should have a scheme of:
"postgresql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DATABASE_NAME>"
"""
engine = create_engine(f'{db_login_info}')

engine.dispose()

# Load covid_all_df dataframe into database
covid_all_df.to_sql(name='covid', con=engine, if_exists='append', index=False)

# Load mask_df dataframe into database
masks_df.to_sql(name='masks', con=engine, if_exists='append', index=False)

# Load cdc_df dataframe into database
cdc_df.to_sql(name='cdc', con=engine, if_exists='append', index=False)

# Load covidtracking_current_df dataframe into database
covidtracking_current_df.to_sql(name='covidtracking_current', con=engine, if_exists='append', index=False)

# Load covidtracking_all_df dataframe into database
covidtracking_all_df.to_sql(name='covidtracking_all', con=engine, if_exists='append', index=False)

# Load county_table_df dataframe into database
county_table_df.to_sql(name='county', con=engine, if_exists='append', index=False)