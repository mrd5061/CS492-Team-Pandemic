import React, { Component } from 'react'
import Chart from './chart';
import DynamicSelect from './charts-select';

let curState =""
let curFitted =[]
let curRate = 0
let g_optID = 'myid'

let stateArrayOfData = [{id:"Alabama",name:"Alabama"},{id:"Alaska",name:"Alaska"},{id:"Arizona",name:"Arizona"},{id:"Arkansas",name:"Arkansas"},{id:"California",name:"California"},{id:"Colorado",name:"Colorado"},{id:"Connecticut",name:"Connecticut"},{id:"Delaware",name:"Delaware"},{id:"District of Columbia",name:"District of Columbia"},{id:"Florida",name:"Florida"},{id:"Georgia",name:"Georgia"},{id:"Hawaii",name:"Hawaii"},{id:"Idaho",name:"Idaho"},{id:"Illinois",name:"Illinois"},{id:"Indiana",name:"Indiana"},{id:"Iowa",name:"Iowa"},{id:"Kansas",name:"Kansas"},{id:"Kentucky",name:"Kentucky"},{id:"Louisiana",name:"Louisiana"},{id:"Maine",name:"Maine"},{id:"Maryland",name:"Maryland"},{id:"Massachusetts",name:"Massachusetts"},{id:"Michigan",name:"Michigan"},{id:"Minnesota",name:"Minnesota"},{id:"Mississippi",name:"Mississippi"},{id:"Missouri",name:"Missouri"},{id:"Montana",name:"Montana"},{id:"Nebraska",name:"Nebraska"},{id:"Nevada",name:"Nevada"},{id:"New Hampshire",name:"New Hampshire"},{id:"New Jersey",name:"New Jersey"},{id:"New Mexico",name:"New Mexico"},{id:"New York",name:"New York"},{id:"North Carolina",name:"North Carolina"},{id:"North Dakota",name:"North Dakota"},{id:"Ohio",name:"Ohio"},{id:"Oklahoma",name:"Oklahoma"},{id:"Oregon",name:"Oregon"},{id:"Pennsylvania",name:"Pennsylvania"},{id:"Rhode Island",name:"Rhode Island"},{id:"South Carolina",name:"South Carolina"},{id:"South Dakota",name:"South Dakota"},{id:"Tennessee",name:"Tennessee"},{id:"Texas",name:"Texas"},{id:"Utah",name:"Utah"},{id:"Vermont",name:"Vermont"},{id:"Virginia",name:"Virginia"},{id:"Washington",name:"Washington"},{id:"West Virginia",name:"West Virginia"},{id:"Wisconsin",name:"Wisconsin"},{id:"Wyoming",name:"Wyoming"}];

let rateArrayOfData = [{id:0.5,name:0.5},{id:1,name:1},{id:2,name:2},{id:3,name:3},{id:4,name:4}];

class Toggle extends React.Component {
  constructor(props) {
    super(props);
    this.state = {isToggleOn: true};

    // This binding is necessary to make `this` work in the callback
    this.handleClick = this.handleClick.bind(this);	
  }
}

export default class Charts extends Component {
  constructor(props) {
    super(props);
    this.state = {
      showCharts: false,
      showCases: true,
      showActive: false,
      showDeaths: false,
      showRecovered: false,
      showBedsPer: false,
      showBedsTotal: false
    }
  }

  handleStateSelectChange = (selectedValue) =>{
	curState = selectedValue
//	console.log("State = " + curState + " Rate = " + curRate)

	if (curState !=	"(Select State)" && curState != ""){
		if (curRate == "(Select Rate)" || curRate == 0) {
//			console.log("Need to select a rate")
		} else {
			this.getFitted(curState, curRate)
		}
	}
  }

  handleRateSelectChange = (selectedValue) =>{
	curRate = selectedValue
//	console.log("State = " + curState + " Rate = " + curRate)
	if (curRate != "(Select Rate)" && curRate != 0) {
		if (curState ==	"(Select State)" || curState == ""){	
//			console.log("Need to select a state")
		} else {
			this.getFitted(curState, curRate)
		}
	}
  }

	getFitted = (curState,curRate) =>{
//		console.log("Getfitted for " + curState + " "+ curRate)
		var fittedChartData = []
		let lineItem=[]
		this.props.day1.forEach(d => {
			if (d.x == curState && d.tRate == curRate) {
				lineItem = {
					x: "Day 1",
					y: d.y,
					style: { fill: '#aaa', fontSize: 10 }				
				}
				fittedChartData.push(lineItem)
			}
		})
		
		this.props.day2.forEach(d => {
			if (d.x == curState && d.tRate == curRate) {
				lineItem = {
					x: "Day 2",
					y: d.y,
					style: { fill: '#aaa', fontSize: 10 }				
				}
				fittedChartData.push(lineItem)
			}
		})
		
		this.props.day3.forEach(d => {
			if (d.x == curState && d.tRate == curRate) {
				lineItem = {
					x: "Day 3",
					y: d.y,
					style: { fill: '#aaa', fontSize: 10 }				
				}
				fittedChartData.push(lineItem)
			}
		})
		
		this.props.day4.forEach(d => {
			if (d.x == curState && d.tRate == curRate) {
				lineItem = {
					x: "Day 4",
					y: d.y,
					style: { fill: '#aaa', fontSize: 10 }				
				}
				fittedChartData.push(lineItem)
			}
		})
		
		this.props.day5.forEach(d => {
			if (d.x == curState && d.tRate == curRate) {
				lineItem = {
					x: "Day 5",
					y: d.y,
					style: { fill: '#aaa', fontSize: 10 }				
				}
				fittedChartData.push(lineItem)
			}
		})
		
		this.props.day6.forEach(d => {
			if (d.x == curState && d.tRate == curRate) {
				lineItem = {
					x: "Day 6",
					y: d.y,
					style: { fill: '#aaa', fontSize: 10 }				
				}
				fittedChartData.push(lineItem)
			}
		})
		
		this.props.day7.forEach(d => {
			if (d.x == curState && d.tRate == curRate) {
				lineItem = {
					x: "Day 7",
					y: d.y,
					style: { fill: '#aaa', fontSize: 10 }				
				}
				fittedChartData.push(lineItem)
			}
		})

		this.setState({ fittedChartData: fittedChartData
					}
				, () => console.log('fitted Chart data loaded'));
			
		curFitted = fittedChartData
//		console.log(fittedChartData)
	}

  handleSelectChange = (selectedValue) =>{
    this.setState({
      selectedValue: selectedValue
    });
  }

  handleClick = () => this.setState({ showCharts: !this.state.showCharts });

  handleCases = () => this.setState({ 
      showCases: true,
      showActive: false,
      showDeaths: false,
      showRecovered: false,
      showBedsPer: false,
      showBedsTotal: false,
      showFitted: false
		});

  handleActive = () => this.setState({ 
      showCases: false,
      showActive: true,
      showDeaths: false,
      showRecovered: false,
      showBedsPer: false,
      showBedsTotal: false,
      showFitted: false
		});

  handleDeaths = () => this.setState({ 
      showCases: false,
      showActive: false,
      showDeaths: true,
      showRecovered: false,
      showBedsPer: false,
      showBedsTotal: false,
      showFitted: false
		});
  handleRecovered = () => this.setState({ 
      showCases: false,
      showActive: false,
      showDeaths: false,
      showRecovered: true,
      showBedsPer: false,
      showBedsTotal: false,
      showFitted: false
		});
  handleBedsPer = () => this.setState({ 
      showCases: false,
      showActive: false,
      showDeaths: false,
      showRecovered: false,
      showBedsPer: true,
      showBedsTotal: false,
      showFitted: false
		});
  handleBedsTotal = () => this.setState({ 
      showCases: false,
      showActive: false,
      showDeaths: false,
      showRecovered: false,
      showBedsPer: false,
      showBedsTotal: true,
      showFitted: false
		});
		
  handleOther = () => this.setState({ 
      showCases: false,
      showActive: false,
      showDeaths: false,
      showRecovered: false,
      showBedsPer: false,
      showBedsTotal: false,
      showFitted: true
		});

  handleState = () => this.setState({ 
      showCases: true,
      showActive: false,
      showDeaths: false,
      showRecovered: false,
      showBedsPer: false,
      showBedsTotal: false,
      showFitted: false
		});

  render() {
    return (
      <>
        {
          this.state.showCharts && (
            <div className="charts-container">
		      <div className="chart" id="chartByCases" style={{display: this.state.showCases ? 'block' : 'none' }}>
                <div className="chart-heading"><span>Current Cases by State</span>
					<button class="chartButton" onClick={this.handleOther}>Fitted Charts</button>
					<br />
					<button class="chartButtonDetail" onClick={this.handleCases}>Chart By Total Cases</button>
					<button class="chartButtonDetail" onClick={this.handleActive}>Chart By Active</button>
					<button class="chartButtonDetail" onClick={this.handleDeaths}>Chart By Deaths</button>
					<button class="chartButtonDetail" onClick={this.handleRecovered}>Chart By Recovered</button>
					<button class="chartButtonDetail" onClick={this.handleBedsPer}>Chart By Beds per 100k</button>
					<button class="chartButtonDetail" onClick={this.handleBedsTotal}>Chart By Total Beds</button>
				</div>
                <Chart filterData={this.props.filterData} data={this.props.caseChart} />
              </div>
			  
			  <div className="chart" id="chartByActive" style={{display: this.state.showActive ? 'block' : 'none' }}>
                <div className="chart-heading"><span>Current Active by State</span>
					<button class="chartButton" onClick={this.handleOther}>Fitted Charts</button>
					<br />
					<button class="chartButtonDetail" onClick={this.handleCases}>Chart By Total Cases</button>
					<button class="chartButtonDetail" onClick={this.handleActive}>Chart By Active</button>
					<button class="chartButtonDetail" onClick={this.handleDeaths}>Chart By Deaths</button>
					<button class="chartButtonDetail" onClick={this.handleRecovered}>Chart By Recovered</button>
					<button class="chartButtonDetail" onClick={this.handleBedsPer}>Chart By Beds per 100k</button>
					<button class="chartButtonDetail" onClick={this.handleBedsTotal}>Chart By Total Beds</button>				
				</div>
                <Chart filterData={this.props.filterData} data={this.props.activeChart} />
              </div>
			  
			  <div className="chart" id="chartByDeaths" style={{display: this.state.showDeaths ? 'block' : 'none' }}>
                <div className="chart-heading"><span>Current Deaths by State</span>
					<button class="chartButton" onClick={this.handleOther}>Fitted Charts</button>
					<br />
					<button class="chartButtonDetail" onClick={this.handleCases}>Chart By Total Cases</button>
					<button class="chartButtonDetail" onClick={this.handleActive}>Chart By Active</button>
					<button class="chartButtonDetail" onClick={this.handleDeaths}>Chart By Deaths</button>
					<button class="chartButtonDetail" onClick={this.handleRecovered}>Chart By Recovered</button>
					<button class="chartButtonDetail" onClick={this.handleBedsPer}>Chart By Beds per 100k</button>
					<button class="chartButtonDetail" onClick={this.handleBedsTotal}>Chart By Total Beds</button>
				</div>
                <Chart filterData={this.props.filterData} data={this.props.deathChart} />
              </div>  
			  
			  <div className="chart" id="chartByRecovered" style={{display: this.state.showRecovered ? 'block' : 'none' }}>
                <div className="chart-heading"><span>Current Recovered by State</span>
					<button class="chartButton" onClick={this.handleOther}>Fitted Charts</button>
					<br />
					<button class="chartButtonDetail" onClick={this.handleCases}>Chart By Total Cases</button>
					<button class="chartButtonDetail" onClick={this.handleActive}>Chart By Active</button>
					<button class="chartButtonDetail" onClick={this.handleDeaths}>Chart By Deaths</button>
					<button class="chartButtonDetail" onClick={this.handleRecovered}>Chart By Recovered</button>
					<button class="chartButtonDetail" onClick={this.handleBedsPer}>Chart By Beds per 100k</button>
					<button class="chartButtonDetail" onClick={this.handleBedsTotal}>Chart By Total Beds</button>
				</div>
                <Chart filterData={this.props.filterData} data={this.props.recoveredChart} />
              </div>

			  <div className="chart" id="chartBedsPer" style={{display: this.state.showBedsPer ? 'block' : 'none' }}>
                <div className="chart-heading"><span>Current Beds per 100k by State</span>
					<button class="chartButton" onClick={this.handleOther}>Fitted Charts</button>
					<br />
					<button class="chartButtonDetail" onClick={this.handleCases}>Chart By Total Cases</button>
					<button class="chartButtonDetail" onClick={this.handleActive}>Chart By Active</button>
					<button class="chartButtonDetail" onClick={this.handleDeaths}>Chart By Deaths</button>
					<button class="chartButtonDetail" onClick={this.handleRecovered}>Chart By Recovered</button>
					<button class="chartButtonDetail" onClick={this.handleBedsPer}>Chart By Beds per 100k</button>
					<button class="chartButtonDetail" onClick={this.handleBedsTotal}>Chart By Total Beds</button>
				</div>
                <Chart filterData={this.props.filterData} data={this.props.bedsPerChart} />
              </div>

			  <div className="chart" id="chartBedsTotal" style={{display: this.state.showBedsTotal ? 'block' : 'none' }}>
                <div className="chart-heading"><span>Current Total Beds by State</span>
					<button class="chartButton" onClick={this.handleOther}>Fitted Charts</button>
					<br />
					<button class="chartButtonDetail" onClick={this.handleCases}>Chart By Total Cases</button>
					<button class="chartButtonDetail" onClick={this.handleActive}>Chart By Active</button>
					<button class="chartButtonDetail" onClick={this.handleDeaths}>Chart By Deaths</button>
					<button class="chartButtonDetail" onClick={this.handleRecovered}>Chart By Recovered</button>
					<button class="chartButtonDetail" onClick={this.handleBedsPer}>Chart By Beds per 100k</button>
					<button class="chartButtonDetail" onClick={this.handleBedsTotal}>Chart By Total Beds</button>
				</div>
                <Chart filterData={this.props.filterData} data={this.props.bedsTotalChart} />
              </div>


			  <div style={{display: this.state.showFitted ? 'block' : 'none'  }}> 			  
				  <div className="chart" id="chartFitted" style={{display: this.state.showFitted ? 'block' : 'none' }}>
					<div className="chart-heading"><span>Fitted Charts</span>
						<button class="chartButton" onClick={this.handleState}>State Charts</button>
						  <div className="Options">
						  <DynamicSelect defaultSel="(Select State)" arrayOfData={stateArrayOfData} optClass={g_optID} onSelectChange={this.handleStateSelectChange} />
							<DynamicSelect defaultSel="(Select Rate)" arrayOfData={rateArrayOfData} optClass={g_optID} onSelectChange={this.handleRateSelectChange} />
						  </div>
						<br />
					</div>
					
					<Chart filterData={this.props.filterData} data={curFitted} />
				  </div>
				</div>
		  </div>
          )
        }

// DM: The below defines the button to launch the charts.
        <div className="btns">
          <div onClick={this.handleClick} className="btn">
            <>
              {
                this.state.showCharts ? (
                  <>
                    <i class="fas hide fa-chart-bar"></i>
                    <div className="diag-strike"></div>
                  </>
                ) : (
                  <i class="fas fa-chart-bar"></i>
                    // <i className="fas fa-chart-area"></i>
                  )
              }
            </>
          </div>
          <>
            {
              this.props.time_filter_selected && <div onClick={this.props.resetFilter} className="btn">
                <i class="fas fa-undo-alt"></i>
              </div>
            }
          </>

        </div>

      </>
    )
  }
}

