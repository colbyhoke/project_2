#!flask/bin/python
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from state_abbrev import abbrev_us_state
from flask import render_template

engine = create_engine('postgresql://covid_db_admin:pass123@localhost:5432/covid_db')
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
        masks_dict["never"] = never
        masks_dict["rarely"] = rarely
        masks_dict["sometimes"] = sometimes
        masks_dict["frequently"] = frequently
        masks_dict["always"] = always

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

    for state, year, week, week_ending_date, all_causes, natural_causes, septicemia, malignant_neoplasms, diabetes, alzheimers, influenza_and_pneumonia, chronic_lower_respiratory, other_diseases_of_respiratory, nephritis_nephrotic_syndrome, symptoms_signs_and_abnormal, diseases_of_heart, cerebrovascular_diseases, covid_19_multiple_causes, covid_19_underlying_cause, flag_otherresp, flag_otherunk, flag_nephr, flag_inflpn, flag_cov19mcod, flag_cov19ucod, flag_sept, flag_diab, flag_alz, flag_clrd, flag_stroke, flag_hd, flag_neopl, flag_allcause, flag_natcause in results:

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
        cdc_dict["flag_otherresp"] = flag_otherresp
        cdc_dict["flag_otherunk"] = flag_otherunk
        cdc_dict["flag_nephr"] = flag_nephr
        cdc_dict["flag_inflpn"] = flag_inflpn
        cdc_dict["flag_cov19mcod"] = flag_cov19mcod
        cdc_dict["flag_cov19ucod"] = flag_cov19ucod
        cdc_dict["flag_sept"] = flag_sept
        cdc_dict["flag_diab"] = flag_diab
        cdc_dict["flag_alz"] = flag_alz
        cdc_dict["flag_clrd"] = flag_clrd
        cdc_dict["flag_stroke"] = flag_stroke
        cdc_dict["flag_hd"] = flag_hd
        cdc_dict["flag_neopl"] = flag_neopl
        cdc_dict["flag_allcause"] = flag_allcause
        cdc_dict["flag_natcause"] = flag_natcause

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
        combined_dict["never"] = never
        combined_dict["rarely"] = rarely
        combined_dict["sometimes"] = sometimes
        combined_dict["frequently"] = frequently
        combined_dict["always"] = always
        combined_dict["county_seat"] = county_seat
        combined_dict["lat"] = lat
        combined_dict["lon"] = lon

        all_data.append(combined_dict)

    return jsonify(all_data)

# Error messages
def bad_request(message):
    response = jsonify({'Error': message})
    response.status_code = 400
    return response

# Comment
if __name__ == '__main__':
    app.run(debug=True)

 