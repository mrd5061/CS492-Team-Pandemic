#Data update script for Team Pandemic
#uses today's date to gather a raw data url for a csv file fomr the Johns Hopkins COVID data repo
#Pulls that cvs file into the database into the import schema
#Then transfers the data via SQL update into the DEATHS, CASES, and RECOVERED tables.
#

import sqlalchemy, datetime
from sqlalchemy import Column, create_engine, select, MetaData,Table,text
import pandas as pd

#dict of states to iterate through. the key represents the STATE_OR_PROVINCE.STATE_ID for each state 
state ={60:'Alabama', 61: 'Alaska', 62: 'Arizona', 63: 'Arkansas', 64: 'California', 65: 'Colorado', 66: 'Connecticut', 67: 'District of Columbia', 68: 'Delaware', 69: 'Florida', 70: 'Georgia', 71: 'Hawaii', 72: 'Idaho', 73: 'Illinois', 74: 'Indiana', 75: 'Iowa', 76: 'Kansas', 77: 'Kentucky', 78: 'Louisiana', 79: 'Maine', 80: 'Maryland', 81: 'Massachusetts' , 82: 'Michigan', 83: 'Minnesota', 84: 'Mississippi', 85: 'Missouri', 86: 'Montana', 87: 'Nebraska', 88: 'Nevada', 89: 'New Hampshire', 90: 'New Jersey', 91: 'New Mexico', 92: 'New York', 93: 'North Carolina', 94: 'North Dakota', 95: 'Ohio', 96: 'Oklahoma', 97: 'Oregon', 98: 'Pennsylvania', 99: 'Rhode Island', 100: 'South Carolina', 101: 'South Dakota', 102: 'Tennessee', 103: 'Texas', 104: 'Utah', 105: 'Vermont', 106: 'Virginia', 107: 'Washington', 108: 'West Virginia', 109: 'Wisconsin', 110: 'Wyoming', 111: 'American Samoa', 112: 'Guam', 113: 'North Mariana Islands', 114: 'Puerto Rico', 115: 'Virgin Isalnds'}

#get the current date
d = datetime.datetime.now()

#connect to the db
engine = sqlalchemy.create_engine("postgres://postgres:pandemic1234@pandemicdb.cehiwrdshmps.us-east-1.rds.amazonaws.com/pandemicdb")

db_conn = engine.connect()

#get the url, replacing the month, day and year in the .csv section with today's date.
url = "http://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/%s-%s-%s.csv"%(d.strftime('%m'), d.strftime('%d'), d.strftime('%Y'))

#read the url into a pandas dataframe
df = pd.read_csv(url, error_bad_lines =False)

#convert the dataframe to a postgresql table in our database under the import schema. Replace the dat if it exists
df.to_sql('report-5-7',schema = 'import', con =engine, if_exists='replace')

#loop through the states and update the data
for k, v in state.items():
	db_conn.execute("""UPDATE "REPORTED_DEATHS" as a	
	SET "NUM_DEATHS" =(select "Deaths" from import."report-5-7" where "Province_State"='%s'), 
	"DATE_REPORTED" = '%s'
	WHERE
	"STATE_ID" = '%s'
	""" %(v,d.strftime('%m/%d/%y'),k))

	db_conn.execute("""UPDATE "REPORTED_CASES" as a	
	SET "NUM_CASES" =(select "Confirmed" from import."report-5-7" where "Province_State"='%s'), 
	"DATE_REPORTED" = '%s'
	WHERE
	"STATE_ID" = '%s'
	""" %(v,d.strftime('%m/%d/%y'),k))

	db_conn.execute("""UPDATE "REPORTED_RECOVERED" as a	
	SET "NUM_RECOVERED" =(select "Recovered" from import."report-5-7" where "Province_State"='%s'), 
	"DATE_REPORTED" = '%s'
	WHERE
	"STATE_ID" = '%s'
	""" %(v,d.strftime('%m/%d/%y'),k))

db_conn.close()
