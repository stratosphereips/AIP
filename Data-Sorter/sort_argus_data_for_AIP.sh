#!/bin/bash -e

yesterday=$(date --date="yesterday" +"%Y/%m/%d")

# Input the location of the data files
input_data_folder=""$yesterday

# Input a location for the output
output_data_folder=""
echo $input_data_folder

#for entry in $input_data_folder/*
#do
#   echo "$entry"
#   ra -r $entry -c , - "dst host " > $output_data_folder$(basename $entry).csv
#done

export output_data_folder
python3 main.py

