import React, { Component } from 'react';
import ReactMapGL, { Marker, Popup, NavigationControl, FullscreenControl } from 'react-map-gl';

import CityPin from './city-pin';
import CityInfo from './city-info';

// Set your mapbox token here
const TOKEN = 'pk.eyJ1IjoiZHZzbTEiLCJhIjoiY2s5cTRxbG90MGdwMzNmcXh5YXVtOXhodSJ9.PoNv2NgKsPOzR93-SbdXhg '; 

const fullscreenControlStyle = {
  position: 'absolute',
  top: 0,
  left: 0,
  padding: '10px'
};

const navStyle = {
  position: 'absolute',
  top: 36,
  left: 0,
  padding: '10px'
};

export default class Mapp extends Component {

  constructor(props) {
    super(props);
    this.state = {
      viewport: {
        width: 100+"vw",
        height: 100+"vh",
        latitude: 39.011902,
        longitude: -98.484245,
        zoom: 4,
        bearing: 0,
        pitch: 0
      },
      popupInfo: null
    };
  }

  _updateViewport = (viewport) => {
    this.setState({ viewport });
  }

  _renderCityMarker = (city, index) => {
    if (city) {
      return (
        <Marker
          key={`marker-${index}`}
          longitude={city.longitude}
          latitude={city.latitude} >
          <CityPin size={20} 
            onClick={() => this.setState({ popupInfo: city })} 
          />
        </Marker>
      );
    }
  }

  _renderPopup() {
    const { popupInfo } = this.state;

    return popupInfo && (
      <Popup tipSize={5}
        anchor="top"
        longitude={popupInfo.longitude}
        latitude={popupInfo.latitude}
        closeOnClick={false}
        onClose={() => this.setState({ popupInfo: null })} >
        <CityInfo info={popupInfo} />
      </Popup>
    );
  }

  render() {

    const { viewport } = this.state;

    return (
      <ReactMapGL
        {...viewport}
		 //DM: Change Map Style Here.
//		mapStyle="mapbox://styles/mapbox/streets-v11"
//		mapStyle="mapbox://styles/mapbox/dark-v10"
		mapStyle="mapbox://styles/mapbox/light-v10"
//		mapStyle="mapbox://styles/mapbox/outdoors-v11"
//		mapStyle="mapbox://styles/dvsm1/ck9sygdjq0b1c1ioe67h5q4y8"
        onViewportChange={this._updateViewport}
        mapboxApiAccessToken={TOKEN} >

        {this.props.cities.map(this._renderCityMarker)}

        {this._renderPopup()}

        <div className="fullscreen" style={fullscreenControlStyle}>
          <FullscreenControl />
        </div>
        <div className="nav" style={navStyle}>
          <NavigationControl onViewportChange={this._updateViewport} />
        </div>

      </ReactMapGL>
    );
  }

}
