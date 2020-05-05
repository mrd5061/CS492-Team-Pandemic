const express = require('express');
const path = require('path');
let csvToJson = require('convert-csv-to-json');
const publicPath = path.join(__dirname, '..', 'dist');

const defaultData = path.join(__dirname, 'data', 'COVID19Data.csv');

const app = express();
const port = process.env.PORT || 3000;

app.use(express.static(publicPath));

app.get('/api/default', (req, res) => {
  let jsonData = csvToJson.fieldDelimiter(',').formatValueByType().getJsonFromCsv(defaultData);
  console.log(`default json = ` + JSON.stringify(jsonData) );
  res.json(jsonData.slice(0,2000));
})

/*
app.get('/api/data', (req, res) => {
  let jsonData = csvToJson.fieldDelimiter(',').formatValueByType().getJsonFromCsv(defaultData);
  console.log(`data json = ` + jsonData.stringify() );
  
  res.json(jsonData.slice(0,2000));
})
*/
app.listen(port, () => {
  console.log(`server listening at ${port}`);
})