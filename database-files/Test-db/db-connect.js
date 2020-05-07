const Pool = require('pg').Pool
var request = require('request');
const pool = new Pool({
  user: 'postgres',
  host: 'pandemicdb.cehiwrdshmps.us-east-1.rds.amazonaws.com',
  database: 'pandemicdb',
  password: 'pandemic1234',
  port: 5432,
})

const getData= (request, response) =>{
	pool.query('SELECT * FROM test."REPORTED_DEATHS"',(error,results)=>{
		if(error){
			throw error
		}
		response.status(200).json(results.rows)
	})

}

module.exports = {getData};
