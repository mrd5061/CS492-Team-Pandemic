#The following queries pull data from the test database schema.
# For all following examples, replace "Wyoming" in the WHERE claues with desired state name

#Select the reported cases from a specific state
SELECT a."NUM_CASES",  b."STATE_NAME" 
FROM test."REPORTED_CASES" as a
	INNER JOIN test."STATE_OR_PROVINCE" as b on a."STATE_ID" = b."STATE_ID"
WHERE "STATE_NAME" = 'Wyoming';

#Select the total beds and beds per 1000 people from a specific state
SELECT a."TOTAL_BEDS", a."BEDS_PER_1K", b."STATE_NAME" 
FROM test."HOSPITAL_BEDS" as a
	INNER JOIN test."STATE_OR_PROVINCE" as b on a."STATE_ID" = b."STATE_ID"
WHERE "STATE_NAME" = 'Wyoming';

#Like above, but just the total beds
SELECT "TOTAL_BEDS", b."STATE_NAME" 
FROM test."HOSPITAL_BEDS" as a
	INNER JOIN test."STATE_OR_PROVINCE" as b on a."STATE_ID" = b."STATE_ID"
WHERE "STATE_NAME" = 'Wyoming';

#Like above, but just the beds per 1k
SELECT "BEDS_PER_1K", b."STATE_NAME" 
FROM test."HOSPITAL_BEDS" as a
	INNER JOIN test."STATE_OR_PROVINCE" as b on a."STATE_ID" = b."STATE_ID"
WHERE "STATE_NAME" = 'Wyoming';

#Update the total beds in hospital beds for a desired state
UPDATE test."HOSPITAL_BEDS"
SET "TOTAL_BEDS" = 2015
	FROM test."STATE_OR_PROVINCE" 
WHERE "STATE_NAME" = 'Wyoming';

#same as above, but for beds per 1k
UPDATE test."HOSPITAL_BEDS"
SET "BEDS_PER_1K" = 9.2
	FROM test."STATE_OR_PROVINCE" 
WHERE "STATE_NAME" = 'Wyoming';

#Returns the Latitude and Longitude of a specified state name
SELECT "LATITUDE", "LONGITUDE"
FROM test."STATE_OR_PROVINCE"	
WHERE "STATE_NAME" = 'Wyoming';

#Returns the Latitude and Longitude of a specified state name
SELECT "POPULATION"
FROM test."STATE_OR_PROVINCE"	
WHERE "STATE_NAME" = 'Wyoming';

#Same as above but for a specified FIPS code.
SELECT "LATITUDE", "LONGITUDE"
FROM test."STATE_OR_PROVINCE"	
WHERE "FIPS" = 56;

#This is applicable if we end up including more geographic regions. 
#Returns the country name for a specified state or province.
SELECT "COUNTRY_NAME"
FROM test."COUNTRIES" as a
	INNER JOIN test."STATE_OR_PROVINCE" as b on a."COUNTRY_ID" = b."COUNTRY_ID"
WHERE b."STATE_NAME" = 'Wyoming';
