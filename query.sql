DROP TABLE IF EXISTS covid, masks, cdc, county, covidtracking_current, covidtracking_all;

-- Create Tables
CREATE TABLE covid (
    date VARCHAR,
    county TEXT,
    state TEXT,
    fips INT,
    cases INT,
    deaths INT,
    PRIMARY KEY (date, fips)
);

CREATE TABLE masks (
    fips INT PRIMARY KEY,
    never FLOAT,
    rarely FLOAT,
    sometimes FLOAT,
    frequently FLOAT,
    always FLOAT
);

CREATE TABLE cdc (
    state TEXT,
    year INT,
    week INT,
    week_ending_date VARCHAR,
    all_causes INT,
    natural_causes INT,
    septicemia INT,
    malignant_neoplasms INT,
    diabetes INT,
    alzheimers INT,
    influenza_and_pneumonia INT,
    chronic_lower_respiratory INT,
    other_diseases_of_respiratory INT,
    nephritis_nephrotic_syndrome INT,
    symptoms_signs_and_abnormal INT,
    diseases_of_heart INT,
    cerebrovascular_diseases INT,
    covid_19_multiple_causes INT,
    covid_19_underlying_cause INT,
    PRIMARY KEY (state, week, year)
);

CREATE TABLE county (
    state TEXT,
    fips INT PRIMARY KEY,
    county TEXT,
    county_seat TEXT,
    lat FLOAT,
    lon FLOAT
);

CREATE TABLE covidtracking_current (
    date INT,
    state TEXT,
    positive INT,
    probable_cases INT,
    negative INT,
    pending INT,
    total_test_results INT,
    hospitalized_currently INT,
    hospitalized_cumulative INT,
    icu_currently INT,
    icu_cumulative INT,
    ventilator_currently INT,
    ventilator_cumulative INT,
    recovered INT,
    data_quality_grade VARCHAR,
    deaths INT,
    hospitalized INT,
    total_tests_viral INT,
    positive_tests_viral INT,
    negative_tests_viral INT,
    positive_cases_viral INT,
    deaths_confirmed INT,
    deaths_probable INT,
    total_test_encounters_viral INT,
    total_tests_people_viral INT,
    total_tests_antibody INT,
    positive_tests_antibody INT,
    negative_tests_antibody INT,
    total_tests_people_antibody INT,
    positive_tests_people_antibody INT,
    negative_tests_people_antibody INT,
    total_tests_people_antigen INT,
    positive_tests_people_antigen INT,
    total_tests_antigen INT,
    positive_tests_antigen INT,
    positive_increase INT,
    negative_increase INT,
    total INT,
    total_test_results_source TEXT,
    total_test_results_increase INT,
    pos_neg INT,
    death_increase INT,
    hospitalized_increase INT,
    PRIMARY KEY (state, date)
);

CREATE TABLE covidtracking_all (
    date INT PRIMARY KEY,
    states TEXT,
    positive INT,
    negative INT,
    pending INT,
    hospitalized_currently INT,
    hospitalized_cumulative INT,
    icu_currently INT,
    icu_cumulative INT,
    ventilator_currently INT,
    ventilator_cumulative INT,
    recovered INT,
    deaths INT,
    hospitalized INT,
    total_test_results INT,
    total INT,
    pos_neg INT,
    death_increase INT,
    hospitalized_increase INT,
    negative_increase INT,
    positive_increase INT,
    total_test_results_increase INT
);