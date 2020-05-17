#Data update script for Team Pandemic
#uses today's date to gather a raw data url for a csv file fomr the Johns Hopkins COVID data repo
#Pulls that cvs file into the database into the import schema
#Then transfers the data via SQL update into the DEATHS, CASES, and RECOVERED tables.
#

import sqlalchemy
from datetime import datetime, timedelta
from sqlalchemy import Column, create_engine, select, MetaData,Table,text
import pandas as pd



#connect to the db
engine = sqlalchemy.create_engine("postgres://postgres:pandemic1234@pandemicdb.cehiwrdshmps.us-east-1.rds.amazonaws.com/pandemicdb")

db_conn = engine.connect()

#Update each of the test tables 
db_conn.execute("""INSERT INTO test."REPORTED_RECOVERED"
  (SELECT * FROM "REPORTED_RECOVERED"
     WHERE "RECOVERED_ID" NOT IN
            (SELECT "RECOVERED_ID" FROM test."REPORTED_RECOVERED"))""")


db_conn.execute("""INSERT INTO test."REPORTED_ACTIVE"
  (SELECT * FROM "REPORTED_ACTIVE"
     WHERE "ACTIVE_ID" NOT IN
            (SELECT "ACTIVE_ID" FROM test."REPORTED_ACTIVE"))""")

db_conn.execute("""INSERT INTO test."REPORTED_DEATHS"
  (SELECT * FROM "REPORTED_DEATHS"
     WHERE "DEATHS_ID" NOT IN
            (SELECT "DEATHS_ID" FROM test."REPORTED_DEATHS"))""")


db_conn.execute("""INSERT INTO test."REPORTED_CASES"
  (SELECT * FROM "REPORTED_CASES"
     WHERE "CASES_ID" NOT IN
            (SELECT "CASES_ID" FROM test."REPORTED_CASES"))""")
	    
db_conn.close()
