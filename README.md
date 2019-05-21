## Description
Use this script to find information on potentially flooding rivers in your area.

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
