//A proof of concept that the database can be connected to and accessed from a node.js server set up. 
//requires installing https://node-postgres.com/ 
//Built in reference to this tutorial: https://blog.logrocket.com/setting-up-a-restful-api-with-node-js-and-postgresql-d96d6fc892d8/
//getData spits out a JSON object full of all the contents of the "REPORTED_DEATHS" table in the pandemicdb database. 


const express = require('express')
const bodyParser = require('body-parser')
const app = express()
const db = require('./db-connect.js')
const port = 3000

app.use(bodyParser.json())
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
)
app.get('/', (request, response) => {
  response.json({ info: 'Node.js, Express, and Postgres API' })
})

app.get('/data',db.getData)


app.listen(port, () => {
  console.log(`App running on port ${port}.`)
})
