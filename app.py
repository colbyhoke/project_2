from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from state_abbrev import abbrev_us_state
from flask import render_template
from config import db_login_info

engine = create_engine(f'{db_login_info}')

Base = automap_base()
Base.prepare(engine, reflect=True)

# Table references
Covid = Base.classes.covid
Masks = Base.classes.masks
Cdc = Base.classes.cdc
County = Base.classes.county
Covidtrackingall = Base.classes.covidtracking_all
Covidtrackingcurrent = Base.classes.covidtracking_current

# Flask setup
app = Flask(__name__)

#########
# 
# Create home route
#
#########
@app.route('/')
def index():
    return render_template("index.html")

#########
# 
# Create counties route
#
#########
@app.route('/counties.html')
def county_index():
    return render_template("counties.html")

#########
# 
# Create API base route
#
#########
@app.route('/api/v1.0/')
def api():
    return render_template("api_routes.html")

#########
# 
# Create map route
# Note: This page is loaded in index.html via an iframe
#
#########
@app.route('/map.html')
def map():
    return render_template("map.html")

#########
# 
# Create chart route
# Note: This page is loaded in counties.html via an iframe
#
#########
@app.route('/chart.html')
def chart():
    return render_template("chart.html")



#########
# 
# Create route to all of the covid data
#
#########

@app.route("/api/v1.0/covid-all")
def covid():
    # Create the session (link) from Python to the DB
    session = Session(engine)

    #Return all covid fields

    results = session.query(Covid.date, Covid.county, Covid.state, Covid.fips, Covid.cases, Covid.deaths).all()
    session.close()

    all_covid = []
    for date, county, state, fips, cases, deaths in results:
        covid_dict = {}
        covid_dict["date"] = date
        covid_dict["county"] = county
        covid_dict["state"] = state
        covid_dict["fips"] = fips
        covid_dict["cases"] = cases
        covid_dict["deaths"] = deaths
        
        all_covid.append(covid_dict)

    return jsonify(all_covid)

#########
# 
# Create route to all of the covid data, but filtered by state input by the user
#
#########

@app.route("/api/v1.0/covid-all/<state_input>")
def covid_state(state_input):
    try:
        # Handle different inputs and capitalizations  
        state_input = state_input.upper()
        state_search = abbrev_us_state[state_input]
        
        # Create the session (link) from Python to the DB
        session = Session(engine)

        # Return all covid fields

        results = session.query(Covid.date, Covid.county, Covid.state, Covid.fips, Covid.cases, Covid.deaths).filter_by(state=state_search).all()
        
        session.close()

        all_covid = []
        for date, county, state, fips, cases, deaths in results:
            covid_dict = {}
            covid_dict["date"] = date
            covid_dict["county"] = county
            covid_dict["state"] = state
            covid_dict["fips"] = fips
            covid_dict["cases"] = cases
            covid_dict["deaths"] = deaths
            
            all_covid.append(covid_dict)

        return jsonify(all_covid)
    
    except:
        return bad_request("State not found. Please format the state its two-letter abbreviation.")

#########
# 
# Create route to all of the mask data
#
#########

@app.route("/api/v1.0/masks")
def masks():
    # Create the session (link) from Python to the DB
    session = Session(engine)

    # Return all mask fields
    results = session.query(Masks.fips, Masks.never, Masks.rarely, Masks.sometimes, Masks.frequently, Masks.always).all()
    session.close()

    all_masks = []
    for fips, never, rarely, sometimes, frequently, always in results:
        masks_dict = {}
        masks_dict["fips"] = fips
        masks_dict["mask_never"] = never
        masks_dict["mask_rarely"] = rarely
        masks_dict["mask_sometimes"] = sometimes
        masks_dict["mask_frequently"] = frequently
        masks_dict["mask_always"] = always

        all_masks.append(masks_dict)
    
    return jsonify(all_masks)


#########
# 
# Create route to all of the cdc data
#
#########
@app.route("/api/v1.0/cdc")
def cdc():
    # Create the session (link) from Python to the DB
    session = Session(engine)

    # Return all cdc fields

    results = session.query(Cdc.state, Cdc.year, Cdc.week, Cdc.week_ending_date, Cdc.all_causes, Cdc.natural_causes, Cdc.septicemia,
    Cdc.malignant_neoplasms, Cdc.diabetes, Cdc.alzheimers, Cdc.influenza_and_pneumonia, Cdc.chronic_lower_respiratory, 
    Cdc.other_diseases_of_respiratory, Cdc.nephritis_nephrotic_syndrome, Cdc.symptoms_signs_and_abnormal,
    Cdc.diseases_of_heart, Cdc.cerebrovascular_diseases, Cdc.covid_19_multiple_causes, Cdc.covid_19_underlying_cause).all()
     
    session.close()

    all_cdc = []

    for state, year, week, week_ending_date, all_causes, natural_causes, septicemia, malignant_neoplasms, diabetes, alzheimers, influenza_and_pneumonia, chronic_lower_respiratory, other_diseases_of_respiratory, nephritis_nephrotic_syndrome, symptoms_signs_and_abnormal, diseases_of_heart, cerebrovascular_diseases, covid_19_multiple_causes, covid_19_underlying_cause in results:

        cdc_dict = {}
        cdc_dict["state"] = state
        cdc_dict["year"] = year
        cdc_dict["week"] = week
        cdc_dict["week_ending_date"] = week_ending_date
        cdc_dict["all_causes"] = all_causes
        cdc_dict["natural_causes"] = natural_causes
        cdc_dict["septicemia"] = septicemia
        cdc_dict["malignant_neoplasms"] = malignant_neoplasms
        cdc_dict["diabetes"] = diabetes
        cdc_dict["alzheimers"] = alzheimers
        cdc_dict["influenza_and_pneumonia"] = influenza_and_pneumonia
        cdc_dict["chronic_lower_respiratory"] = chronic_lower_respiratory
        cdc_dict["other_diseases_of_respiratory"] = other_diseases_of_respiratory
        cdc_dict["nephritis_nephrotic_syndrome"] = nephritis_nephrotic_syndrome
        cdc_dict["symptoms_signs_and_abnormal"] = symptoms_signs_and_abnormal
        cdc_dict["diseases_of_heart"] = diseases_of_heart
        cdc_dict["cerebrovascular_diseases"] = cerebrovascular_diseases
        cdc_dict["covid_19_multiple_causes"] = covid_19_multiple_causes
        cdc_dict["covid_19_underlying_cause"] = covid_19_underlying_cause

        all_cdc.append(cdc_dict)

    return jsonify(all_cdc)

#########
# 
# Create route to all of the county data
#
#########

@app.route("/api/v1.0/counties")
def counties():
    # Create the session (link) from Python to the DB
    session = Session(engine)

    # Return all county fields
    results = session.query(County.state, County.fips, County.county, County.county_seat, County.lat, County.lon).all()
    print(results)
    session.close()

    all_counties = []

    for state, fips, county, county_seat, lat, lon in results:
        county_dict = {}

        county_dict["state"] = state
        county_dict["fips"] = fips
        county_dict["county"] = county 
        county_dict["county_seat"] = county_seat
        county_dict["lat"] = lat
        county_dict["lon"] = lon

        all_counties.append(county_dict)

    return jsonify(all_counties)

#########
# 
# Create route to all of the county data, but filtered by state input by the user
#
#########
@app.route("/api/v1.0/counties/<state_input>")
def counties_state(state_input):
    
    try:
        # Handle different inputs and capitalizations
        state_search = state_input.upper()
        
        # Create the session (link) from Python to the DB
        session = Session(engine)

        # Return all county fields
        results = session.query(County.state, County.fips, County.county, County.county_seat, County.lat, 
        County.lon).filter_by(state=state_search).all()
        
        session.close()

        all_counties = []

        for state, fips, county, county_seat, lat, lon in results:
            county_dict = {}

            county_dict["state"] = state
            county_dict["fips"] = fips
            county_dict["county"] = county 
            county_dict["county_seat"] = county_seat
            county_dict["lat"] = lat
            county_dict["lon"] = lon

            all_counties.append(county_dict)

        return jsonify(all_counties)    

    except:
        return bad_request("State not found. Please format the state its two-letter abbreviation.")

#########
# 
# Create route to the covidtracking-all data table
#
#########
@app.route("/api/v1.0/covidtracking-all")
def covidtracking_all():
    # Create the session (link) from Python to the DB
    session = Session(engine)

    # Return all covidtracking-all fields

    results = session.query(Covidtrackingall.date, Covidtrackingall.states, Covidtrackingall.positive,
    Covidtrackingall.negative, Covidtrackingall.pending, Covidtrackingall.hospitalized_currently,
    Covidtrackingall.hospitalized_cumulative, Covidtrackingall.icu_currently, Covidtrackingall.icu_cumulative,
    Covidtrackingall.ventilator_currently, Covidtrackingall.ventilator_cumulative, Covidtrackingall.recovered,
    Covidtrackingall.deaths, Covidtrackingall.hospitalized, Covidtrackingall.total_test_results, Covidtrackingall.total,
    Covidtrackingall.pos_neg, Covidtrackingall.death_increase, Covidtrackingall.hospitalized_increase,
    Covidtrackingall.negative_increase, Covidtrackingall.positive_increase, Covidtrackingall.total_test_results_increase).all()

    session.close()

    all_covidtracking_all = []

    for date, states, positive, negative, pending, hospitalized_currently, hospitalized_cumulative, icu_currently, icu_cumulative, ventilator_currently, ventilator_cumulative, recovered, deaths, hospitalized, total_test_results, total, pos_neg, death_increase, hospitalized_increase, negative_increase, positive_increase, total_test_results_increase in results:
        covidtracking_all_dict = {}

        covidtracking_all_dict["date"] = date
        covidtracking_all_dict["states"] = states
        covidtracking_all_dict["positive"] = positive
        covidtracking_all_dict["negative"] = negative
        covidtracking_all_dict["pending"] = pending
        covidtracking_all_dict["hospitalized_currently"] = hospitalized_currently
        covidtracking_all_dict["hospitalized_cumulative"] = hospitalized_cumulative
        covidtracking_all_dict["icu_currently"] = icu_currently
        covidtracking_all_dict["icu_cumulative"] = icu_cumulative
        covidtracking_all_dict["ventilator_currently"] = ventilator_currently
        covidtracking_all_dict["ventilator_cumulative"] = ventilator_cumulative
        covidtracking_all_dict["recovered"] = recovered
        covidtracking_all_dict["deaths"] = deaths
        covidtracking_all_dict["hospitalized"] = hospitalized
        covidtracking_all_dict["total_test_results"] = total_test_results
        covidtracking_all_dict["total"] = total
        covidtracking_all_dict["pos_neg"] = pos_neg
        covidtracking_all_dict["death_increase"] = death_increase
        covidtracking_all_dict["hospitalized_increase"] = hospitalized_increase
        covidtracking_all_dict["negative_increase"] = negative_increase
        covidtracking_all_dict["positive_increase"] = positive_increase
        covidtracking_all_dict["total_test_results_increase"] = total_test_results_increase

        all_covidtracking_all.append(covidtracking_all_dict)

    return jsonify(all_covidtracking_all)

#########
# 
# Create route to the covidtracking-all data table
#
#########
@app.route("/api/v1.0/covidtracking-all/<date_input>")
def covidtracking_all_date(date_input):
    try:

        # Create the session (link) from Python to the DB
        session = Session(engine)

        # Return all covidtracking-all fields

        results = session.query(Covidtrackingall.date, Covidtrackingall.states, Covidtrackingall.positive,
        Covidtrackingall.negative, Covidtrackingall.pending, Covidtrackingall.hospitalized_currently,
        Covidtrackingall.hospitalized_cumulative, Covidtrackingall.icu_currently, Covidtrackingall.icu_cumulative,
        Covidtrackingall.ventilator_currently, Covidtrackingall.ventilator_cumulative, Covidtrackingall.recovered,
        Covidtrackingall.deaths, Covidtrackingall.hospitalized, Covidtrackingall.total_test_results, Covidtrackingall.total,
        Covidtrackingall.pos_neg, Covidtrackingall.death_increase, Covidtrackingall.hospitalized_increase,
        Covidtrackingall.negative_increase, Covidtrackingall.positive_increase, Covidtrackingall.total_test_results_increase).filter_by(date=date_input).all()

        session.close()

        all_covidtracking_all = []

        for date, states, positive, negative, pending, hospitalized_currently, hospitalized_cumulative, icu_currently, icu_cumulative, ventilator_currently, ventilator_cumulative, recovered, deaths, hospitalized, total_test_results, total, pos_neg, death_increase, hospitalized_increase, negative_increase, positive_increase, total_test_results_increase in results:
            covidtracking_all_dict = {}

            covidtracking_all_dict["date"] = date
            covidtracking_all_dict["states"] = states
            covidtracking_all_dict["positive"] = positive
            covidtracking_all_dict["negative"] = negative
            covidtracking_all_dict["pending"] = pending
            covidtracking_all_dict["hospitalized_currently"] = hospitalized_currently
            covidtracking_all_dict["hospitalized_cumulative"] = hospitalized_cumulative
            covidtracking_all_dict["icu_currently"] = icu_currently
            covidtracking_all_dict["icu_cumulative"] = icu_cumulative
            covidtracking_all_dict["ventilator_currently"] = ventilator_currently
            covidtracking_all_dict["ventilator_cumulative"] = ventilator_cumulative
            covidtracking_all_dict["recovered"] = recovered
            covidtracking_all_dict["deaths"] = deaths
            covidtracking_all_dict["hospitalized"] = hospitalized
            covidtracking_all_dict["total_test_results"] = total_test_results
            covidtracking_all_dict["total"] = total
            covidtracking_all_dict["pos_neg"] = pos_neg
            covidtracking_all_dict["death_increase"] = death_increase
            covidtracking_all_dict["hospitalized_increase"] = hospitalized_increase
            covidtracking_all_dict["negative_increase"] = negative_increase
            covidtracking_all_dict["positive_increase"] = positive_increase
            covidtracking_all_dict["total_test_results_increase"] = total_test_results_increase

            all_covidtracking_all.append(covidtracking_all_dict)

        return jsonify(all_covidtracking_all)
    
    except:
        return bad_request("Date not found. Either the date has no associated data or it was formatted incorrectly. Please format the date as YYYYMMDD (ex. 20201006).")

#########
# 
# Create route to the covidtracking-all data table
#
#########
@app.route("/api/v1.0/covidtracking-current")
def covidtracking_current():
    # Create the session (link) from Python to the DB
    session = Session(engine)

    # Return all covidtracking-current fields

    results = session.query(Covidtrackingcurrent.date, Covidtrackingcurrent.state, Covidtrackingcurrent.positive,
    Covidtrackingcurrent.probable_cases, Covidtrackingcurrent.negative, Covidtrackingcurrent.pending,
    Covidtrackingcurrent.total_test_results, Covidtrackingcurrent.hospitalized_currently, Covidtrackingcurrent.hospitalized_cumulative,
    Covidtrackingcurrent.icu_currently, Covidtrackingcurrent.icu_cumulative, Covidtrackingcurrent.ventilator_currently,
    Covidtrackingcurrent.ventilator_cumulative, Covidtrackingcurrent.recovered, Covidtrackingcurrent.data_quality_grade, Covidtrackingcurrent.deaths,
    Covidtrackingcurrent.hospitalized, Covidtrackingcurrent.total_tests_viral, Covidtrackingcurrent.positive_tests_viral,
    Covidtrackingcurrent.negative_tests_viral, Covidtrackingcurrent.positive_cases_viral, Covidtrackingcurrent.deaths_confirmed,
    Covidtrackingcurrent.deaths_probable, Covidtrackingcurrent.total_test_encounters_viral, Covidtrackingcurrent.total_tests_people_viral,
    Covidtrackingcurrent.total_tests_antibody, Covidtrackingcurrent.positive_tests_antibody, Covidtrackingcurrent.negative_tests_antibody,
    Covidtrackingcurrent.total_tests_people_antibody, Covidtrackingcurrent.positive_tests_people_antibody, Covidtrackingcurrent.negative_tests_people_antibody,
    Covidtrackingcurrent.total_tests_people_antigen, Covidtrackingcurrent.positive_tests_people_antigen, Covidtrackingcurrent.total_tests_antigen,
    Covidtrackingcurrent.positive_tests_antigen, Covidtrackingcurrent.positive_increase, Covidtrackingcurrent.negative_increase, Covidtrackingcurrent.total,
    Covidtrackingcurrent.total_test_results_source, Covidtrackingcurrent.total_test_results_increase, Covidtrackingcurrent.pos_neg,
    Covidtrackingcurrent.death_increase, Covidtrackingcurrent.hospitalized_increase).all()
    session.close()
    
    all_covidtracking_current = []

    for date, state, positive, probable_cases, negative, pending, total_test_results, hospitalized_currently, hospitalized_cumulative, icu_currently, icu_cumulative, ventilator_currently, ventilator_cumulative, recovered, data_quality_grade, deaths, hospitalized, total_tests_viral, positive_tests_viral, negative_tests_viral, positive_cases_viral, deaths_confirmed, deaths_probable, total_test_encounters_viral, total_tests_people_viral, total_tests_antibody, positive_tests_antibody, negative_tests_antibody, total_tests_people_antibody, positive_tests_people_antibody, negative_tests_people_antibody, total_tests_people_antigen, positive_tests_people_antigen, total_tests_antigen, positive_tests_antigen, positive_increase, negative_increase, total, total_test_results_source, total_test_results_increase, pos_neg, death_increase, hospitalized_increase in results:
        
        covidtracking_current_dict = {}

        covidtracking_current_dict["date"] = date
        covidtracking_current_dict["state"] = state
        covidtracking_current_dict["positive"] = positive
        covidtracking_current_dict["probable_cases"] = probable_cases
        covidtracking_current_dict["negative"] = negative
        covidtracking_current_dict["pending"] = pending
        covidtracking_current_dict["total_test_results"] = total_test_results
        covidtracking_current_dict["hospitalized_currently"] = hospitalized_currently
        covidtracking_current_dict["hospitalized_cumulative"] = hospitalized_cumulative
        covidtracking_current_dict["icu_currently"] = icu_currently
        covidtracking_current_dict["icu_cumulative"] = icu_cumulative
        covidtracking_current_dict["ventilator_currently"] = ventilator_currently
        covidtracking_current_dict["ventilator_cumulative"] = ventilator_cumulative
        covidtracking_current_dict["recovered"] = recovered
        covidtracking_current_dict["data_quality_grade"] = data_quality_grade
        covidtracking_current_dict["deaths"] = deaths
        covidtracking_current_dict["hospitalized"] = hospitalized
        covidtracking_current_dict["total_tests_viral"] = total_tests_viral
        covidtracking_current_dict["positive_tests_viral"] = positive_tests_viral
        covidtracking_current_dict["negative_tests_viral"] = negative_tests_viral
        covidtracking_current_dict["positive_cases_viral"] = positive_cases_viral
        covidtracking_current_dict["deaths_confirmed"] = deaths_confirmed
        covidtracking_current_dict["deaths_probable"] = deaths_probable
        covidtracking_current_dict["total_test_encounters_viral"] = total_test_encounters_viral
        covidtracking_current_dict["total_tests_people_viral"] = total_tests_people_viral
        covidtracking_current_dict["total_tests_antibody"] = total_tests_antibody
        covidtracking_current_dict["positive_tests_antibody"] = positive_tests_antibody
        covidtracking_current_dict["negative_tests_antibody"] = negative_tests_antibody
        covidtracking_current_dict["total_tests_people_antibody"] = total_tests_people_antibody
        covidtracking_current_dict["positive_tests_people_antibody"] = positive_tests_people_antibody
        covidtracking_current_dict["negative_tests_people_antibody"] = negative_tests_people_antibody
        covidtracking_current_dict["total_tests_people_antigen"] = total_tests_people_antigen
        covidtracking_current_dict["positive_tests_people_antigen"] = positive_tests_people_antigen
        covidtracking_current_dict["total_tests_antigen"] = total_tests_antigen
        covidtracking_current_dict["positive_tests_antigen"] = positive_tests_antigen
        covidtracking_current_dict["positive_increase"] = positive_increase
        covidtracking_current_dict["negative_increase"] = negative_increase
        covidtracking_current_dict["total"] = total
        covidtracking_current_dict["total_test_results_source"] = total_test_results_source
        covidtracking_current_dict["total_test_results_increase"] = total_test_results_increase
        covidtracking_current_dict["pos_neg"] = pos_neg
        covidtracking_current_dict["death_increase"] = death_increase
        covidtracking_current_dict["hospitalized_increase"] = hospitalized_increase

        all_covidtracking_current.append(covidtracking_current_dict)

    return jsonify(all_covidtracking_current)

#########
# 
# Create route to the covidtracking-all data table, but filtered by state input by the user
#
#########
@app.route("/api/v1.0/covidtracking-current/<state_input>")
def covidtracking_current_state(state_input):
    try:
        # Handle different inputs and capitalizations
        state_search = state_input.upper()
    
        # Create the session (link) from Python to the DB
        session = Session(engine)

        # Return all covidtracking-current fields

        results = session.query(Covidtrackingcurrent.date, Covidtrackingcurrent.state, Covidtrackingcurrent.positive,
        Covidtrackingcurrent.probable_cases, Covidtrackingcurrent.negative, Covidtrackingcurrent.pending,
        Covidtrackingcurrent.total_test_results, Covidtrackingcurrent.hospitalized_currently, Covidtrackingcurrent.hospitalized_cumulative,
        Covidtrackingcurrent.icu_currently, Covidtrackingcurrent.icu_cumulative, Covidtrackingcurrent.ventilator_currently,
        Covidtrackingcurrent.ventilator_cumulative, Covidtrackingcurrent.recovered, Covidtrackingcurrent.data_quality_grade, Covidtrackingcurrent.deaths,
        Covidtrackingcurrent.hospitalized, Covidtrackingcurrent.total_tests_viral, Covidtrackingcurrent.positive_tests_viral,
        Covidtrackingcurrent.negative_tests_viral, Covidtrackingcurrent.positive_cases_viral, Covidtrackingcurrent.deaths_confirmed,
        Covidtrackingcurrent.deaths_probable, Covidtrackingcurrent.total_test_encounters_viral, Covidtrackingcurrent.total_tests_people_viral,
        Covidtrackingcurrent.total_tests_antibody, Covidtrackingcurrent.positive_tests_antibody, Covidtrackingcurrent.negative_tests_antibody,
        Covidtrackingcurrent.total_tests_people_antibody, Covidtrackingcurrent.positive_tests_people_antibody, Covidtrackingcurrent.negative_tests_people_antibody,
        Covidtrackingcurrent.total_tests_people_antigen, Covidtrackingcurrent.positive_tests_people_antigen, Covidtrackingcurrent.total_tests_antigen,
        Covidtrackingcurrent.positive_tests_antigen, Covidtrackingcurrent.positive_increase, Covidtrackingcurrent.negative_increase, Covidtrackingcurrent.total,
        Covidtrackingcurrent.total_test_results_source, Covidtrackingcurrent.total_test_results_increase, Covidtrackingcurrent.pos_neg,
        Covidtrackingcurrent.death_increase, Covidtrackingcurrent.hospitalized_increase).filter_by(state=state_search).all()
        session.close()
        
        all_covidtracking_current = []

        for date, state, positive, probable_cases, negative, pending, total_test_results, hospitalized_currently, hospitalized_cumulative, icu_currently, icu_cumulative, ventilator_currently, ventilator_cumulative, recovered, data_quality_grade, deaths, hospitalized, total_tests_viral, positive_tests_viral, negative_tests_viral, positive_cases_viral, deaths_confirmed, deaths_probable, total_test_encounters_viral, total_tests_people_viral, total_tests_antibody, positive_tests_antibody, negative_tests_antibody, total_tests_people_antibody, positive_tests_people_antibody, negative_tests_people_antibody, total_tests_people_antigen, positive_tests_people_antigen, total_tests_antigen, positive_tests_antigen, positive_increase, negative_increase, total, total_test_results_source, total_test_results_increase, pos_neg, death_increase, hospitalized_increase in results:
            
            covidtracking_current_dict = {}

            covidtracking_current_dict["date"] = date
            covidtracking_current_dict["state"] = state
            covidtracking_current_dict["positive"] = positive
            covidtracking_current_dict["probable_cases"] = probable_cases
            covidtracking_current_dict["negative"] = negative
            covidtracking_current_dict["pending"] = pending
            covidtracking_current_dict["total_test_results"] = total_test_results
            covidtracking_current_dict["hospitalized_currently"] = hospitalized_currently
            covidtracking_current_dict["hospitalized_cumulative"] = hospitalized_cumulative
            covidtracking_current_dict["icu_currently"] = icu_currently
            covidtracking_current_dict["icu_cumulative"] = icu_cumulative
            covidtracking_current_dict["ventilator_currently"] = ventilator_currently
            covidtracking_current_dict["ventilator_cumulative"] = ventilator_cumulative
            covidtracking_current_dict["recovered"] = recovered
            covidtracking_current_dict["data_quality_grade"] = data_quality_grade
            covidtracking_current_dict["deaths"] = deaths
            covidtracking_current_dict["hospitalized"] = hospitalized
            covidtracking_current_dict["total_tests_viral"] = total_tests_viral
            covidtracking_current_dict["positive_tests_viral"] = positive_tests_viral
            covidtracking_current_dict["negative_tests_viral"] = negative_tests_viral
            covidtracking_current_dict["positive_cases_viral"] = positive_cases_viral
            covidtracking_current_dict["deaths_confirmed"] = deaths_confirmed
            covidtracking_current_dict["deaths_probable"] = deaths_probable
            covidtracking_current_dict["total_test_encounters_viral"] = total_test_encounters_viral
            covidtracking_current_dict["total_tests_people_viral"] = total_tests_people_viral
            covidtracking_current_dict["total_tests_antibody"] = total_tests_antibody
            covidtracking_current_dict["positive_tests_antibody"] = positive_tests_antibody
            covidtracking_current_dict["negative_tests_antibody"] = negative_tests_antibody
            covidtracking_current_dict["total_tests_people_antibody"] = total_tests_people_antibody
            covidtracking_current_dict["positive_tests_people_antibody"] = positive_tests_people_antibody
            covidtracking_current_dict["negative_tests_people_antibody"] = negative_tests_people_antibody
            covidtracking_current_dict["total_tests_people_antigen"] = total_tests_people_antigen
            covidtracking_current_dict["positive_tests_people_antigen"] = positive_tests_people_antigen
            covidtracking_current_dict["total_tests_antigen"] = total_tests_antigen
            covidtracking_current_dict["positive_tests_antigen"] = positive_tests_antigen
            covidtracking_current_dict["positive_increase"] = positive_increase
            covidtracking_current_dict["negative_increase"] = negative_increase
            covidtracking_current_dict["total"] = total
            covidtracking_current_dict["total_test_results_source"] = total_test_results_source
            covidtracking_current_dict["total_test_results_increase"] = total_test_results_increase
            covidtracking_current_dict["pos_neg"] = pos_neg
            covidtracking_current_dict["death_increase"] = death_increase
            covidtracking_current_dict["hospitalized_increase"] = hospitalized_increase

            all_covidtracking_current.append(covidtracking_current_dict)

        return jsonify(all_covidtracking_current)
    
    except:
        return bad_request("State not found. Please format the state its two-letter abbreviation.")

# Error message
def bad_request(message):
    response = jsonify({'Error': message})
    response.status_code = 400
    return response

# Run the app
if __name__ == '__main__':
    app.run(debug=True)