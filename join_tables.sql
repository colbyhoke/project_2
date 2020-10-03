create table combined as
SELECT covid.date, covid.county, covid.state, covid.cases, covid.deaths, 
	masks.fips, masks.never, masks.rarely, masks.sometimes, masks.frequently, masks.always,
	county.county_seat, county.lat, county.lon
FROM covid
INNER JOIN masks ON masks.fips = covid.fips
INNER JOIN county ON county.fips = masks.fips;


ALTER TABLE combined
ADD CONSTRAINT Primarykeyname PRIMARY KEY (date, fips);