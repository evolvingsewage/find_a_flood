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

### Windows
```
.\windows\setup.ps1
.\windows\run.ps1 <city> <state> <radius>
```

`setup.ps1` creates `venv\` with the `py` launcher and installs
`requirements.txt`. `run.ps1` runs `find_a_flood.py` through that venv,
forwarding any arguments (e.g. `.\windows\run.ps1 Austin TX 25 --category
minor`).

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
  --category {low_threshold,no_flooding,action,minor,moderate,major,obs_not_current,not_defined,out_of_service}
                        The category of flooding to search for.
  --refresh_data        Whether or not to rebuild the database of results.

```

When the script runs, it will populate a database with gauge data from NOAA's National Water Prediction Service, then
it navigates that database to find floods within the parameters given by the user.

## Credits
* River Level Information - https://water.noaa.gov/
* Distance on Globe from Haversine Formula - https://andrew.hedges.name/experiments/haversine/
