#!/bin/bash

# Please Input location of current instance
output_folder=

# Please Input location of input data files
input_data_folder=

# Export all variables so they can be accessed by AIP.py
export output_folder
export input_data_folder

directory_of_AIP=$(pwd)

python3 $directory_of_AIP/Main/Select_Modules.py

for entry in $input_data_folder/*
do
   cp "$entry" $output_folder/Input_Data/
   python3 $directory_of_AIP/Main/AIP.py
done
