SELECT covid.date, covid.county, covid.state, covid.fips, covid.cases, covid.deaths, 
	masks.fips, masks.never, masks.rarely, masks.sometimes, masks.frequently, masks.always
FROM covid
INNER JOIN masks ON masks.fips = covid.fips

