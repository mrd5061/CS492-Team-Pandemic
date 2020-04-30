
#Select the total beds and beds per 1000 people from a specific state
#Replace Wyoming with desired state
SELECT total_beds, beds_per_1k, b.state_name 
FROM "HOSPITAL_BEDS" as a
	INNER JOIN "STATE_OR_PROVINCE" as b on a.state_id = b.state_id
WHERE state_name = 'Wyoming';

#Like above, but just the total beds
SELECT total_beds, b.state_name 
FROM "HOSPITAL_BEDS" as a
	INNER JOIN "STATE_OR_PROVINCE" as b on a.state_id = b.state_id
WHERE state_name = 'Wyoming';

#Like above, but just the beds per 1k
SELECT beds_per_1k, b.state_name 
FROM "HOSPITAL_BEDS" as a
	INNER JOIN "STATE_OR_PROVINCE" as b on a.state_id = b.state_id
WHERE state_name = 'Wyoming';

#Update the total beds in hospital beds for a desired state
UPDATE "HOSPITAL_BEDS"
SET total_beds = 2015
	FROM"STATE_OR_PROVINCE" 
WHERE state_name = 'Wyoming';

#same as above, but for beds per 1k
UPDATE "HOSPITAL_BEDS"
SET beds_per_1k = 2015
	FROM"STATE_OR_PROVINCE" 
WHERE state_name = 'Wyoming';

#Returns the Latitude and Longitude of a specified state name
SELECT latitude, longitude
FROM "STATE_OR_PROVINCE"	
WHERE state_name = 'Wyoming';

#Same as above but for a specified FIPS code.
SELECT latitude, longitude
FROM "STATE_OR_PROVINCE"	
WHERE "FIPS" = 56;

#This is applicable if we end up including more geographic regions. 
#Returns the country name for a specified state or province.
SELECT country_name
FROM "COUNTRIES" as a
	INNER JOIN "STATE_OR_PROVINCE" as b on a.country_id = b.country_id
WHERE a.state_name = 'Wyoming';
