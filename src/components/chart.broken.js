import React, { Component } from 'react';

import { XYPlot, XAxis, YAxis, VerticalRectSeries, VerticalBarSeries, LabelSeries } from 'react-vis';

class BarGraph extends Component {

  constructor(props){
    super(props);
    this.state = {
      chartDomain_y : 0
    }
  }

  handleValueClick = (event) => {
// DM: This event handler returns the x and y data.
    console.log(event);
	alert ("You clicked on " + event.x + "!")
  }

  render() {
    const {data} = this.props;

    return (
      <XYPlot 
		width={1500} 
		height={400} 
		margin={{bottom: 150, left: 75}} 
		xType="ordinal"
      >
        <XAxis tickFormat={v => `${v}`} tickLabelAngle={-45}  />
        <YAxis />
        <VerticalBarSeries
          data={data}
         strokeWidth={2}
          stroke="#222"
          fill="#ED0A3F"
          colorType="literal"
          onValueClick={this.handleValueClick}
        />
        <LabelSeries
          data={data.map(obj => {
            return { ...obj, label: obj.y.toString() }
          })}

          labelAnchorX="middle"
          labelAnchorY="text-after-edge"
        />
		
      </XYPlot>
    );
  }
}

export default BarGraph;