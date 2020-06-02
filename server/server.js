const express = require('express');
const path = require('path');
const fs = require('fs');
const fetch = require("node-fetch");
const app = express();
const port = process.env.PORT || 3000;


const publicPath = path.join(__dirname, '..', 'dist');
const covidDataFile = path.join(__dirname, 'data', 'COVID19Data.csv');
const fittedDataFile = path.join(__dirname, 'data', 'fittedData.csv');
const stateCoord = path.join(__dirname, 'data', 'stateMaping.csv');
const fileDir = path.join(__dirname, 'data', 'cdcDataSet.csv'); // Download data of CDC 
const logFile = path.join(__dirname, 'data', 'logfile.txt'); 

//DM: Database side.
const { Pool, Client } = require('pg')

let csvToJson = require('convert-csv-to-json');

app.use(express.static(publicPath));

function logData(logMsg){
/* DM: Log informtion to a file.	
*/
	var date = new Date();

    var month = date.getMonth() + 1;
    var day = date.getDate();
    var hour = date.getHours();
    var min = date.getMinutes();
    var sec = date.getSeconds();
	var curLogFile = ""

    month = (month < 10 ? "0" : "") + month;
    day = (day < 10 ? "0" : "") + day;
    hour = (hour < 10 ? "0" : "") + hour;
    min = (min < 10 ? "0" : "") + min;
    sec = (sec < 10 ? "0" : "") + sec;

    var newMsg = date.getFullYear() + month + day + "-" +  hour + ":" + min + ":" + sec + " - " + logMsg + "\r\n";
	
	console.log(newMsg)

	try {
	  curLogFile = fs.readFileSync(logFile, 'utf8')
	} catch (err) {
	  console.error(err)
	}	
	
	var newLogFile = curLogFile + newMsg
	fs.writeFile(logFile, newLogFile, function (err) {
	  if (err) return console.log(err)
	});


	return 0
}

app.get('/api/csvpins', (req, res) => {
// DM: Grab CSV file and convert to JSON.
// DM: If database was not there, will use old file.
	logData("Getting Pin JSON file");
	let jsonData = csvToJson.fieldDelimiter(',').formatValueByType().getJsonFromCsv(covidDataFile);

	res.json(jsonData.slice(0,2000));
})

app.get('/api/csvfit', (req, res) => {
// DM: Grab CSV file and convert to JSON.
// DM: If database was not there, will use old file.
	logData("Getting Fitted JSON file");
	let jsonData = csvToJson.fieldDelimiter(',').formatValueByType().getJsonFromCsv(fittedDataFile);

	res.json(jsonData.slice(0,2000));
})

app.get('/api/pindata', (req, res) => { 
//DM: Get data from database. If successfull, replace CSV file.
	let dbEnviron = 'public' // public or test
	
	var sqlquery = "SELECT \
			C.\"COUNTRY_NAME\" \
			, SOP.\"STATE_NAME\" \
			, SOP.\"LATITUDE\" \
			, SOP.\"LONGITUDE\" \
			, RR.\"NUM_RECOVERED\" \
			, RD.\"NUM_DEATHS\" \
			, RC.\"NUM_CASES\" \
			, RA.\"NUM_ACTIVE\" \
			, HB.\"BEDS_PER_1K\" \
			, HB.\"TOTAL_BEDS\" \
			FROM " + dbEnviron + ".\"STATE_OR_PROVINCE\" SOP  \
			join " + dbEnviron + ".\"COUNTRIES\" C on C.\"COUNTRY_ID\"=SOP.\"COUNTRY_ID\" \
			join " + dbEnviron + ".\"REPORTED_RECOVERED\" RR on RR.\"STATE_ID\"=SOP.\"STATE_ID\" \
			join " + dbEnviron + ".\"REPORTED_DEATHS\" RD on RD.\"STATE_ID\"=SOP.\"STATE_ID\" \
			join " + dbEnviron + ".\"REPORTED_CASES\" RC on RC.\"STATE_ID\"=SOP.\"STATE_ID\" \
			join " + dbEnviron + ".\"REPORTED_ACTIVE\" RA on RA.\"STATE_ID\"=SOP.\"STATE_ID\" \
			join " + dbEnviron + ".\"HOSPITAL_BEDS\" HB on HB.\"STATE_ID\"=SOP.\"STATE_ID\" \
			WHERE RR.\"DATE_REPORTED\" = ( SELECT MAX(\"DATE_REPORTED\") from " + dbEnviron + ".\"REPORTED_RECOVERED\" WHERE RR.\"STATE_ID\" = \"STATE_ID\") \
			and  RD.\"DATE_REPORTED\" = ( SELECT MAX(\"DATE_REPORTED\") from " + dbEnviron + ".\"REPORTED_DEATHS\" WHERE RD.\"STATE_ID\" = \"STATE_ID\") \
			and  RC.\"DATE_REPORTED\" = ( SELECT MAX(\"DATE_REPORTED\") from " + dbEnviron + ".\"REPORTED_CASES\" WHERE RC.\"STATE_ID\" = \"STATE_ID\") \
			and  RA.\"DATE_REPORTED\" = ( SELECT MAX(\"DATE_REPORTED\") from " + dbEnviron + ".\"REPORTED_ACTIVE\" WHERE RA.\"STATE_ID\" = \"STATE_ID\") \
			order by  C.\"COUNTRY_NAME\", SOP.\"STATE_NAME\"; "
	logData("PIN SQL Query = " + sqlquery);

	var client = new Client({
	  user: 'postgres',
	  host: 'pandemicdb.cehiwrdshmps.us-east-1.rds.amazonaws.com',
	  database: 'pandemicdb',
	  password: 'pandemic1234',
	  port: 5432,
	})
	client.connect()
	client.query(sqlquery, (err, res) => {
	if (err) {
		logData("pg returned an error:" +  err.code)
		throw error;
	}
	if (res) {
		//DM: Update the CSV file.
		var csvFile = "COUNTRY_NAME,STATE_NAME,LATITUDE,LONGITUDE,NUM_RECOVERED,NUM_DEATHS,NUM_CASES,NUM_ACTIVE,BEDS_PER_1K,TOTAL_BEDS\r\n"
		
	    const data = res.rows;
		var csvLine = "";

		//DM: Loop through each row returned and write them out the the file.
		data.forEach(row => {
			csvLine = row.COUNTRY_NAME + "," + row.STATE_NAME + "," + row.LATITUDE + "," + row.LONGITUDE + "," + row.NUM_RECOVERED + "," +  row.NUM_DEATHS + "," + row.NUM_CASES + "," + row.NUM_ACTIVE + "," + row.BEDS_PER_1K + "," + row.TOTAL_BEDS + "\r\n" 			
			csvFile += csvLine
		})

		fs.writeFile(covidDataFile, csvFile, function (err) {
		  if (err) return console.log(err)
		  	logData('New Pin file written.')
		});		
	}			
		
	client.end()
	})	
})


app.get('/api/fitdata', (req, res) => { 
//DM: Get data from database. If successfull, replace CSV file.
	let dbEnviron = 'public' // public or test
	
	var sqlquery = "SELECT distinct \
						C.\"COUNTRY_NAME\" \
						, SOP.\"STATE_NAME\" \
						, SOP.\"LATITUDE\" \
						, SOP.\"LONGITUDE\" \
						, FD.\"TRANS_RATE\" \
						, round(FD.\"DAY_1\",0) as DAY1 \
						, round(FD.\"DAY_2\",0) as DAY2 \
						, round(FD.\"DAY_3\",0) as DAY3 \
						, round(FD.\"DAY_4\",0) as DAY4 \
						, round(FD.\"DAY_5\",0) as DAY5 \
						, round(FD.\"DAY_6\",0) as DAY6 \
						, round(FD.\"DAY_7\",0) as DAY7 \
						FROM " + dbEnviron + ".\"STATE_OR_PROVINCE\" SOP \
						join " + dbEnviron + ".\"FITTED_DATA\" FD on FD.\"STATE_ID\"=SOP.\"STATE_ID\" \
						join " + dbEnviron + ".\"COUNTRIES\" C on C.\"COUNTRY_ID\"=SOP.\"COUNTRY_ID\" \
						WHERE FD.\"DATE_REPORTED\" = ( SELECT MAX(\"DATE_REPORTED\") from " + dbEnviron + ".\"FITTED_DATA\" WHERE FD.\"STATE_ID\" = \"STATE_ID\") \
						order by C.\"COUNTRY_NAME\", SOP.\"STATE_NAME\", FD.\"TRANS_RATE\"; "

	logData("Fitted SQL Query = " + sqlquery);

	var client = new Client({
	  user: 'postgres',
	  host: 'pandemicdb.cehiwrdshmps.us-east-1.rds.amazonaws.com',
	  database: 'pandemicdb',
	  password: 'pandemic1234',
	  port: 5432,
	})
	client.connect()
	client.query(sqlquery, (err, res) => {
	if (err) {
		logData("pg returned an error:" +  err.code)
		throw error;
	}
	if (res) {
		//DM: Update the CSV file.
		var csvFile = "COUNTRY_NAME,STATE_NAME,LATITUDE,LONGITUDE,TRANS_RATE,DAY1,DAY2,DAY3,DAY4,DAY5,DAY6,DAY7\r\n"
		
	    const data = res.rows;
		var csvLine = "";

		//DM: Loop through each row returned and write them out the the file.
		data.forEach(row => {
			csvLine = row.COUNTRY_NAME + "," + row.STATE_NAME + "," + row.LATITUDE + "," + row.LONGITUDE + "," + row.TRANS_RATE + "," +  row.day1 + "," + row.day2 + "," + row.day3 + "," + row.day4 + "," + row.day5 + "," + row.day6 + "," + row.day7 + "\r\n" 			
			csvFile += csvLine
		})

		fs.writeFile(fittedDataFile, csvFile, function (err) {
		  if (err) return console.log(err)
		  	logData('New Fitted file written.')
		});		
	}			
		
	client.end()
	})	
})


/*
app.get('/api/data-old', (req, res) => { 
//DM: NO LONGER USING.
//DM: Grab CDC file and download it to the data directory. 

//console.log ("at api/data");
  var cdcURL = 'https://www.cdc.gov/covid-data-tracker/Content/CoronaViewJson_01/US_MAP_DATA.csv';
	fetch(cdcURL)
	  .then(res => res.blob()) // Gets the response and returns it as a blob
	  .then(blob => {
		blobstream = blob.stream();
		blobstream.pipe(fs.createWriteStream(fileDir))
	});
	
	//DM: Get the mapping file to the long and lat.
	let jsonState = csvToJson.fieldDelimiter(',').formatValueByType().getJsonFromCsv(stateCoord);
	
	var longlat = '';
	var myFile = '';
	
	fs.readFile(fileDir, 'utf8', function(err, data){   
    	fLines = data.split("\r\n");
		var lCount = 0;
		fLines.forEach(function(fLine){
			lCount++;
			if (lCount <= 2 )   { //DM: We have the first line which is a date.
			//DM: Changed the data to have 2 non-data lines
				
			}else{
				if (lCount == 3) { //DM: Change some headers
					fLine = fLine.replace("Total Cases", "totcase");
					fLine = fLine.replace("Total Death", "totdeath");
					fLine = fLine.replace("CasesInLast7Days", "last7");
					fLine = fLine.replace("RatePer100000", "per100k");

					longlat = ",state_long,state_lat\r\n";
				} else {
				
					tLine = fLine.split(","); //DM Split out the line by comm to grab the abbr
//console.log ("TLine [0] = " + tLine[0]);
					longlat = '';
					
					for (var i = 0; i < jsonState.length; i++){
					  // look for the entry with a matching `state_appr` value
					  if (jsonState[i].state_abbr == tLine[0]){
						 // we found it
						// obj[i].name is the matched result
						longlat = "," + jsonState[i].state_long + "," + jsonState[i].state_lat + "\r\n";
//console.log ("jsopn = " + longlat);
					  }
					}
				}

				myFile += fLine + longlat; 
			}				
//console.log("Line " + lCount+ " - " + fLine); 
		});

		fs.writeFile(covidDataFile, myFile, function (err) {
		  if (err) return console.log(err);
//		  console.log('File written');
		});

	}); 
})
*/

app.listen(port, () => {
  console.log(`server listening at ${port}`);
})