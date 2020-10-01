SELECT covid.date, covid.county, covid.state, covid.fips, covid.cases, covid.deaths, 
	masks.fips, masks.never, masks.rarely, masks.sometimes, masks.frequently, masks.always,
	county.state, county.fips, county.county, county.county_seat, county.lat, county.lon
FROM covid
INNER JOIN masks ON masks.fips = covid.fips
INNER JOIN county ON county.fips = masks.fips


