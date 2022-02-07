#!/bin/bash -e

yesterday=$(date --date="yesterday" +"%Y/%m/%d")

# Input the location of the data files
input_data_folder=" "$yesterday

# Input a location for the argus flows that have been converted to csv
output_data_folder=" "

# A location for the aggregated output data file
results_file=" "

cd $output_data_folder
rm *

echo $input_data_folder/*

for entry in $input_data_folder/*
do
   # Check if there are any connections to the lab devices (This is here due to an error where the whole script will stop if there are not)
   echo "$entry"
   connection_counts=$(ra -F /etc/ra.conf -n -Z b -r $entry - "dst host ...." | wc -l)
   echo $connection_counts
   if [ "$connection_counts" -ne "0" ];
   then
   	# If there are connections to the lab, extract them to a csv
   	echo Extracting data
   	test=$(ra -r $entry -c , - "dst host ....." > $output_data_folder$(basename $entry).csv)
   else
   	# If there are no connections, skip this file
   	echo Skipping
   	continue
   fi
done

# Export the output loctions
export output_data_folder
export results_file

# Call the python file that will extract the data we want
python3 main.py
