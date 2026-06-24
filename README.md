## Description
Use this script to find information on potentially flooding rivers in your area.

## Prerequisites
Prerequisites are installed into a virtual environment, don't mess up your own
environment to run this! Run everything from the python/ directory of this
repository. I wrote everything with that in mind.

Create a virtual environment (e.g. `python -m venv venv`) and install
`requirements.txt` into it. River gauge data is downloaded automatically by
`find_a_flood.py` on first run (or with `--refresh_data`) from NOAA's National
Water Prediction Service; no separate download script is needed.

## Usage

```
usage: find_a_flood.py [-h]
                       [--category {low_threshold,no_flooding,action,minor,moderate,major,obs_not_current,not_defined,out_of_service}]
                       [--refresh_data]
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

When the script runs, it will populate a database with gauge data from NOAA's National Water Prediction Service, then
it navigates that database to find floods within the parameters given by the user.

## Credits
* River Level Information - https://water.noaa.gov/
* Distance on Globe from Haversine Formula - https://andrew.hedges.name/experiments/haversine/
