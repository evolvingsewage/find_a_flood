#!/bin/bash

# river bash script
# author: Blake
# downloads river data and prints the current river hight, flood stages, and predected river hight

main () {
	# set up variables
	SILENT=false
	setupQuiet
	downloadRiverData
	prepareData
}

setupQuiet () {
	exec 7>&1	# save a copy of the current stdout
	exec >/dev/null	# redirect everyones else's stdout to /dev/null
	SILENT=true
}

downloadRiverData () {
	# Download current river data from the goverment
	wget --quiet https://water.weather.gov/ahps/download.php?data=kmz_obs

}

prepareData () {
	# Rename the download and unzip the file, then remove the zip
	mv 'download.php?data=kmz_obs' riverOBS.kmz
	unzip riverOBS.kmz
	rm riverOBS.kmz

	# rename the file
	mv ahps_national_obs.kml riverOBS.xml

	# find the last line of the file
	lastline=`wc -l < riverOBS.xml`

	# remove the second and the last line
	sed -i "2d;${lastline}d" "riverOBS.xml"
}


main "$@"
