# CS492-Team-Pandemic
This is a team based project where we will develop models and an interactive web interface similar to https://covidactnow.org/ which allows users to choose from multiple parameters in calculating the models. The models will be based on publicly available data from multiple sources, import this data to a database, calculate statistical models, and display the data and models in a tabular format and clickable, map-based format.

## Installation

Our Website is hosted at http://mcnall.dyndns.org:3000/. 
## Usage

The website features an interactive map of the United States. Each state has a centroid marker that, when clicked, will display data regarding the number of covid related deaths, active cases, total hospital beds, and hospital beds per 1k residents. The site will also display an interactive chart displaing the projection results of our model. The user will be able to view how differning levels of strictness regarding state stay at home ordinances could affect the number of future COVID cases. 

## Built With
  * React - UI, Visualization graphics
  * Postgresql - Database system
  * AWS
      * RDS - database hosting
      * Lightsail - backend server
  * [JHU CSSE COVID-19 Dataset](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data#jhu-csse-covid-19-dataset) - primary data source 

## Authors

  * Meghan Dougherty
  * Amanda Lawrence
  * Daniel McNall
