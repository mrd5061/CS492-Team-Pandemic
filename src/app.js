import React, { Component } from 'react';
import './app.scss';
import Map from './components/map';
import axios from 'axios';
import Charts from './components/charts';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      data: [],
      download_data: [],
      filtered_data: [],
      infection_data: [],
      time_filter: "",
    }
  }

  handleFiltering = (time) => {
    const newData = [...this.state.data].filter(d => d.time_hour === time);
    this.setState({ time_filter: time, filtered_data: newData });
  }

  handleResetFilter = () => this.setState({ time_filter: ""});

	 componentDidMount() {

//DM: Grab the Database file from the server.
	 axios.get('/api/pindata').then(({ download_data }) => {
	 });

//DM: Grab the CSV file
    axios.get('/api/csvpins').then(({ data }) => {
		var stateCount = 0;
		let validData = [];
		let caseChartData = [];
		let deathChartData = [];
		let activeChartData = [];
		let recoveredChartData = [];
		let bedsPerChartData=[];
		let totalBedsChartData=[];

		var sName
		var nDeaths
		var nCases
		var nActive
		var nRecovered
		var bPer
		var bTot
		
	// DM: This is where we take the JSON and parse it out for the map. d is each row of the JSON.
		  data.forEach(d => {
			if ( d.LONGITUDE != "null" && d.LATITUDE !== "null") { // Have a location d.NUM_DEATHS != "NULL" &&

				
				stateCount+=1
	// DM: Validate the data. If null, set to unknown.			
				if (d.STATE_NAME == "null") {sName = "unknown"} else {sName=d.STATE_NAME}
				if (d.NUM_DEATHS == "null") {nDeaths = "unknown"} else {nDeaths=d.NUM_DEATHS}
				if (d.NUM_CASES == "null") {nCases = "unknown"} else {nCases=d.NUM_CASES}
				if (d.NUM_ACTIVE == "null") {nActive = "unknown"} else {nActive=d.NUM_ACTIVE}
				if (d.NUM_RECOVERED == "null") {nRecovered = "unknown"} else {nRecovered=d.NUM_RECOVERED}
				if (d.BEDS_PER_1K == "null") {bPer = "unknown"} else {bPer=d.BEDS_PER_1K}
				if (d.TOTAL_BEDS == "null") {bTot = "unknown"} else {bTot=d.TOTAL_BEDS}
		
	//		console.log ("Long = " + d.LONGITUDE  + " Lat = " + d.LATITUDE);	
			  let validItem = {
				name: sName + "\r\n" + nDeaths + " Deaths \r\n" + nCases + " Infected \r\n"  + nActive + " Active Test \r\n" + nRecovered + " Recovered \r\n" + bPer + " Beds per 1K \r\n" + bTot + " Total Beds \r\n",            longitude: d.LONGITUDE,
				latitude: d.LATITUDE
	//            time_hour: parseInt(d.booking_created.split(' ')[1].split(':')[0], 10)
			  }
			  validData.push(validItem);
			}
		  })
	// DM Pins are built

	// DM: Build out charts using react-vis (D3 overlay).
			const state_occur = Array.from(Array(stateCount), (x) => 0);

		var i =0;
		//Chart Data....
		  data.forEach(d => {
			i+=1

		//DM: Set to zero if null
			if (d.STATE_NAME == "null") {sName = "unknown"} else {sName=d.STATE_NAME}
			if (d.NUM_DEATHS == "null") {nDeaths = 0} else {nDeaths=d.NUM_DEATHS}
			if (d.NUM_CASES == "null") {nCases = 0} else {nCases=d.NUM_CASES}
			if (d.NUM_ACTIVE == "null") {nActive = 0} else {nActive=d.NUM_ACTIVE}
			if (d.NUM_RECOVERED == "null") {nRecovered = 0} else {nRecovered=d.NUM_RECOVERED}
			if (d.BEDS_PER_1K == "null") {bPer = 0} else {bPer=d.BEDS_PER_1K}
			if (d.TOTAL_BEDS == "null") {bTot = 0} else {bTot=d.TOTAL_BEDS}

		
		//DM: Build out the line. Get the state and the cases.
			let caseItem = {
				x: sName,
				y: nCases,
				style: { fill: '#aaa', fontSize: 10 }
			}

			let deathItem = {
				x: sName,
				y: nDeaths,
				style: { fill: '#aaa', fontSize: 10 }
			}
			
			let activeItem = {
				x: sName,
				y: nActive,
				style: { fill: '#aaa', fontSize: 10 }
			}

			let recoveredItem = {
				x: sName,
				y: nRecovered,
				style: { fill: '#aaa', fontSize: 10 }
			}

			let bedsPerItem = {
				x: sName,
				y: bPer,
				style: { fill: '#aaa', fontSize: 10 }
			}

			let totalBedsItem = {
				x: sName,
				y: bTot,
				style: { fill: '#aaa', fontSize: 10 }
			}
			
	//DM: Create the chart array
			caseChartData.push(caseItem)
			deathChartData.push(deathItem)
			activeChartData.push(activeItem)
			recoveredChartData.push(recoveredItem)
			bedsPerChartData.push(bedsPerItem)
			totalBedsChartData.push(totalBedsItem)
		  });

	//DM - Show data as a JSON output - console.log ("JSON=" + JSON.stringify(recoveredChartData))
		  this.setState({ loading: false,
						data: validData,
						case_data: caseChartData,
						active_data: activeChartData,
						recovered_data: recoveredChartData,
						death_data: deathChartData,
						bedsPer_data: bedsPerChartData,
						bedsTotal_data: totalBedsChartData
						}
				, () => console.log('loaded'));
    }).catch(e => console.log(e));


	//DM: Grab the fitted Database file from the server.
	 axios.get('/api/fitdata').then(({ download_data }) => {
	 });



// Grab the fitted CSV file
    axios.get('/api/csvfit').then(({ data }) => {

	var stateCount = 0;
	let day1ChartData = [];
	let day2ChartData = [];
	let day3ChartData = [];
	let day4ChartData = [];
	let day5ChartData = [];
	let day6ChartData = [];
	let day7ChartData = [];
	let stateList = [];
	let stateListShort = [];
	let tRateList = [];
	let tRateListShort = [];
	
	var sName
	var transRate
	var nDay1
	var nDay2
	var nDay3
	var nDay4
	var nDay5
	var nDay6
	var nDay7

// DM: Build out charts using react-vis (D3 overlay).
	const state_occur = Array.from(Array(stateCount), (x) => 0);

	var i =0;
	//Chart Data....
      data.forEach(d => {
		i+=1

	//DM: Set to zero if null
		if (d.STATE_NAME == "null") {sName = "unknown"} else {sName=d.STATE_NAME}
		if (d.TRANS_RATE == "null") {transRate = "unknown"} else {transRate=d.TRANS_RATE}
		if (d.DAY1 == "null") {nDay1 = 0} else {nDay1=d.DAY1}
		if (d.DAY2 == "null") {nDay2 = 0} else {nDay2=d.DAY2}
		if (d.DAY3 == "null") {nDay3 = 0} else {nDay3=d.DAY3}
		if (d.DAY4 == "null") {nDay4 = 0} else {nDay4=d.DAY4}
		if (d.DAY5 == "null") {nDay5 = 0} else {nDay5=d.DAY5}
		if (d.DAY6 == "null") {nDay6 = 0} else {nDay6=d.DAY6}
		if (d.DAY7 == "null") {nDay7 = 0} else {nDay7=d.DAY7}
		
	//DM: Build out the line. Get the state and the cases.
		let nDay1Item = {
			tRate: transRate,
			x: sName,
			y: nDay1,
			style: { fill: '#aaa', fontSize: 10 }
		}

		let nDay2Item = {
			tRate: transRate,
			x: sName,
			y: nDay2,
			style: { fill: '#aaa', fontSize: 10 }
		}
		
		let nDay3Item = {
			tRate: transRate,
			x: sName,
			y: nDay3,
			style: { fill: '#aaa', fontSize: 10 }
		}

		let nDay4Item = {
			tRate: transRate,
			x: sName,
			y: nDay4,
			style: { fill: '#aaa', fontSize: 10 }
		}

		let nDay5Item = {
			tRate: transRate,
			x: sName,
			y: nDay5,
			style: { fill: '#aaa', fontSize: 10 }
		}

		let nDay6Item = {
			tRate: transRate,
			x: sName,
			y: nDay6,
			style: { fill: '#aaa', fontSize: 10 }
		}

		let nDay7Item = {
			tRate: transRate,
			x: sName,
			y: nDay7,
			style: { fill: '#aaa', fontSize: 10 }
		}

		if (!stateList.includes(sName, 0)){
			stateList.push(sName)
			let stateItem = {
				id: sName,
				name: sName
			}	
			stateList.push(stateItem)
			stateListShort.push(stateItem)
		}
		
		
		
		if (!tRateList.includes(transRate, 0)){
			tRateList.push(transRate)
			let tRateItem = {
				id: transRate,
				name: transRate
			}
			tRateListShort.push(tRateItem)			
		}

//DM: Create the chart array. This should be an array of the states with a filter??...
		day1ChartData.push(nDay1Item)
		day2ChartData.push(nDay2Item)
		day3ChartData.push(nDay3Item)
		day4ChartData.push(nDay4Item)
		day5ChartData.push(nDay5Item)
		day6ChartData.push(nDay6Item)
		day7ChartData.push(nDay7Item)
      });

//DM - Show data as a JSON output - console.log ("JSON=" + JSON.stringify(recoveredChartData))
//console.log ("Fitted JSON=" + JSON.stringify(day1ChartData))
// console.log ("stateListShort=" +	JSON.stringify(stateListShort))
//console.log ("tRateList=" +	JSON.stringify(tRateList))


      this.setState({ loading: false,
					stateList: stateList,
					stateListShort: JSON.stringify(stateListShort),
					tRateList: tRateList,
					tRateListShort: JSON.stringify(tRateListShort),
					day1: day1ChartData,
					day2: day2ChartData,
					day3: day3ChartData,
					day4: day4ChartData,
					day5: day5ChartData,
					day6: day6ChartData,
					day7: day7ChartData
					}
				, () => console.log('data loaded'));
			
    }).catch(e => console.log(e));
		
  }
  render() {
    return (
      <>
        {
          this.state.loading ? (
            <div className="loading"></div>
          ) : (
              <>
                <Map cities={this.state.time_filter.length === 0 ? this.state.data : this.state.filtered_data} />

                <Charts
					resetFilter={this.handleResetFilter}
					filterData={this.handleFiltering} 
					caseChart={this.state.case_data} 
					activeChart={this.state.active_data} 
					deathChart={this.state.death_data} 
					recoveredChart={this.state.recovered_data}
					bedsPerChart={this.state.bedsPer_data}
					bedsTotalChart={this.state.bedsTotal_data}
					day1={this.state.day1}
					day2={this.state.day2}
					day3={this.state.day3}
					day4={this.state.day4}
					day5={this.state.day5}
					day6={this.state.day6}
					day7={this.state.day7}
					tRateList={this.state.tRateListShort}
					stateList={this.state.stateListShort}
						/>

              </>
            )
        }
      </>
    )
  }

}

export default App;