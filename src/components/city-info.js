import React from 'react';

//DM: This controls the pop-up box.
const CityInfo = (props) => {
//  console.log(props.info.name);
  return (
    <div style={{ color: "#000"}} > 
     <pre> {props.info.name} </pre>
    </div>
  );
}

export default CityInfo;