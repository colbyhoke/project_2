#!flask/bin/python
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from state_abbrev import abbrev_us_state
from flask import render_template

rds_connection_string = 'covid_db_admin:pass123@localhost:5432/covid_db'
#rds_connection_string = 'wewgmdkmixbost:2867215a1a0078b7b97755002ee58726a435d9667c75357935b55e35d15779b9@ec2-52-21-247-176.compute-1.amazonaws.com:5432/davqjt1jvosgp8'
engine = create_engine(f'postgresql://{rds_connection_string}')

Base = automap_base()
Base.prepare(engine, reflect=True)

# Table references
Covid = Base.classes.covid
Masks = Base.classes.masks
Cdc = Base.classes.cdc
County = Base.classes.county
Combined = Base.classes.combined

# Flask setup
app = Flask(__name__)

#########
# 
# Create home route
# Link to all available routes
#
#########
@app.route('/')
def index():
    return render_template("index.html")

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
# Create route to all of the covid data
#
#########

@app.route("/api/v1.0/covid-all")
def covid():
    # Create the session (link) from Python to the DB
    session = Session(engine)

    #Return all covid stuff

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

        # Return all covid stuff

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

    # Return all mask stuff
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

    # Return all cdc stuff

    results = session.query(Cdc.state, Cdc.year, Cdc.week, Cdc.week_ending_date, Cdc.all_causes, Cdc.natural_causes, Cdc.septicemia,
    Cdc.malignant_neoplasms, Cdc.diabetes, Cdc.alzheimers, Cdc.influenza_and_pneumonia, Cdc.chronic_lower_respiratory, 
    Cdc.other_diseases_of_respiratory, Cdc.nephritis_nephrotic_syndrome, Cdc.symptoms_signs_and_abnormal,
    Cdc.diseases_of_heart, Cdc.cerebrovascular_diseases, Cdc.covid_19_multiple_causes, Cdc.covid_19_underlying_cause, 
    Cdc.flag_otherresp, Cdc.flag_otherunk, Cdc.flag_nephr, Cdc.flag_inflpn, Cdc.flag_cov19mcod, Cdc.flag_cov19ucod, Cdc.flag_sept,
    Cdc.flag_diab, Cdc.flag_alz, Cdc.flag_clrd, Cdc.flag_stroke, Cdc.flag_hd, Cdc.flag_neopl, Cdc.flag_allcause, Cdc.flag_natcause).all()
     
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

    # Return all county stuff
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

        # Return all county stuff
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
# Create route to the combined data table
#
#########

@app.route("/api/v1.0/combined-data")
def combined():
    # Create the session (link) from Python to the DB
    session = Session(engine)

    # Return all county stuff
    results = session.query(Combined.date, Combined.county, Combined.state, Combined.cases, Combined.deaths, 
    Combined.fips, Combined.never, Combined.rarely, Combined.sometimes, Combined.frequently, Combined.always, 
    Combined.county_seat, Combined.lat, Combined.lon).all()

    session.close()

    all_data = []

    for date, county, state, cases, deaths, fips, never, rarely, sometimes, frequently, always, county_seat, lat, lon in results:
        combined_dict = {}

        combined_dict["date"] = date
        combined_dict["county"] = county 
        combined_dict["state"] = state
        combined_dict["cases"] = cases
        combined_dict["deaths"] = deaths
        combined_dict["fips"] = fips
        combined_dict["mask_never"] = never
        combined_dict["mask_rarely"] = rarely
        combined_dict["mask_sometimes"] = sometimes
        combined_dict["mask_frequently"] = frequently
        combined_dict["mask_always"] = always
        combined_dict["county_seat"] = county_seat
        combined_dict["lat"] = lat
        combined_dict["lon"] = lon

        all_data.append(combined_dict)

    return jsonify(all_data)

#########
# 
# Create route to the combined data table, but filtered by state input by the user
#
#########

@app.route("/api/v1.0/combined-data/<state_input>")
def combined_state(state_input):
    try:
        # Handle different inputs and capitalizations  
        state_input = state_input.upper()
        state_search = abbrev_us_state[state_input]
        
        # Create the session (link) from Python to the DB
        session = Session(engine)

        # Return all county stuff
        results = session.query(Combined.date, Combined.county, Combined.state, Combined.cases, Combined.deaths, 
        Combined.fips, Combined.never, Combined.rarely, Combined.sometimes, Combined.frequently, Combined.always, 
        Combined.county_seat, Combined.lat, Combined.lon).filter_by(state=state_search).all()

        session.close()

        all_data = []

        for date, county, state, cases, deaths, fips, never, rarely, sometimes, frequently, always, county_seat, lat, lon in results:
            combined_dict = {}

            combined_dict["date"] = date
            combined_dict["county"] = county 
            combined_dict["state"] = state
            combined_dict["cases"] = cases
            combined_dict["deaths"] = deaths
            combined_dict["fips"] = fips
            combined_dict["mask_never"] = never
            combined_dict["mask_rarely"] = rarely
            combined_dict["mask_sometimes"] = sometimes
            combined_dict["mask_frequently"] = frequently
            combined_dict["mask_always"] = always
            combined_dict["county_seat"] = county_seat
            combined_dict["lat"] = lat
            combined_dict["lon"] = lon

            all_data.append(combined_dict)

        return jsonify(all_data)
    
    except:
        return bad_request("State not found. Please format the state its two-letter abbreviation.")


# Error messages
def bad_request(message):
    response = jsonify({'Error': message})
    response.status_code = 400
    return response

# Comment
if __name__ == '__main__':
    app.run(debug=True)

 