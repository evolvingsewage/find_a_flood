## Description
Use this script to find information on potentially flooding rivers in your area.

## Prerequisites
Prerequisites are installed by virtualenv, don't mess up your own environment
to run this! Run everything from the main directory of this repository. I wrote
everything with that in mind. 

Before running anything, run the venv\_creator.sh script to create the virtual
environment. Then, run the river.sh script to pull the latest river flooding
data.

## Usage

```
usage: find_a_flood.py [-h]
                       [--category {Low_Water,No_Flooding,Action_Stage,Minor_Stage,Moderate_Stage,Minor_Stage,Observations_are_not_current,Not_Defined}]
                       [--referesh-data]
                       city state radius

positional arguments:
  city                  The name of a city.
  state                 The two letter abbreviation of the state the city is
                        in.
  radius                The search radius, in miles.

optional arguments:
  -h, --help            show this help message and exit
  --category {Low_Water,No_Flooding,Action_Stage,Minor_Stage,Moderate_Stage,Minor_Stage,Observations_are_not_current,Not_Defined}
                        The category of flooding to search for.
  --referesh-data       Whether or not to rebuild the database of results.

```

When the script runs, it will populate a database with the information from the XML file provided by the National Weather Service, then
it navigates that database to find floods within the parameters given by the user. 

## Credits
* River Level Information - https://water.weather.gov/ahps/
* Distance on Globe from Haversine Formula - https://andrew.hedges.name/experiments/haversine/
