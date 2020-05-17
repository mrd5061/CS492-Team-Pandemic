#Data update script for Team Pandemic
#uses today's date to gather a raw data url for a csv file fomr the Johns Hopkins COVID data repo
#Pulls that cvs file into the database into the import schema
#Then transfers the data via SQL update into the DEATHS, CASES, and RECOVERED tables.
#

import sqlalchemy
from datetime import datetime, timedelta
from sqlalchemy import Column, create_engine, select, MetaData,Table,text
import pandas as pd

#dict of states to iterate through. the key represents the STATE_OR_PROVINCE.STATE_ID for each state 
state ={60:'Alabama', 61: 'Alaska', 62: 'Arizona', 63: 'Arkansas', 64: 'California', 65: 'Colorado', 66: 'Connecticut', 67: 'District of Columbia', 68: 'Delaware', 69: 'Florida', 70: 'Georgia', 71: 'Hawaii', 72: 'Idaho', 73: 'Illinois', 74: 'Indiana', 75: 'Iowa', 76: 'Kansas', 77: 'Kentucky', 78: 'Louisiana', 79: 'Maine', 80: 'Maryland', 81: 'Massachusetts' , 82: 'Michigan', 83: 'Minnesota', 84: 'Mississippi', 85: 'Missouri', 86: 'Montana', 87: 'Nebraska', 88: 'Nevada', 89: 'New Hampshire', 90: 'New Jersey', 91: 'New Mexico', 92: 'New York', 93: 'North Carolina', 94: 'North Dakota', 95: 'Ohio', 96: 'Oklahoma', 97: 'Oregon', 98: 'Pennsylvania', 99: 'Rhode Island', 100: 'South Carolina', 101: 'South Dakota', 102: 'Tennessee', 103: 'Texas', 104: 'Utah', 105: 'Vermont', 106: 'Virginia', 107: 'Washington', 108: 'West Virginia', 109: 'Wisconsin', 110: 'Wyoming', 111: 'American Samoa', 112: 'Guam', 113: 'North Mariana Islands', 114: 'Puerto Rico', 115: 'Virgin Isalnds'}

#connect to the db
engine = sqlalchemy.create_engine("postgres://postgres:pandemic1234@pandemicdb.cehiwrdshmps.us-east-1.rds.amazonaws.com/pandemicdb")
#get the current date
d = datetime.now()

#get yesterday's date
#d = datetime.now()-timedelta(days=2)

#convert the datetime object to the specific format required by the csv file
dString = d.strftime("%-m/%-d/%y")
db_conn = engine.connect()

#get the url, replacing the month, day and year in the .csv section with today's date.
url = "http://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"

#read the url into a pandas dataframe
df = pd.read_csv(url, error_bad_lines =False)

#convert the dataframe to a postgresql table in our database under the import schema. Replace the dat if it exists
df.to_sql('times_report_confirmed',schema = 'import', con =engine, if_exists='replace')

#loop through the states and update the data
for k, v in state.items():
	db_conn.execute("""INSERT INTO "REPORTED_CASES"	
	("STATE_ID","NUM_CASES","DATE_REPORTED")
	VALUES ( {},(SELECT SUM("{}") FROM import.times_report_confirmed WHERE "Province_State" = '{}'),'{}')""".format(k,dString,v,dString,v))

db_conn.close()
