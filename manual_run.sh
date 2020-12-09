#!/bin/bash
answer1="Yes"
answer2="No"
answer3="1"
answer4="2"

echo "............................"
echo "Please Select a option from the menu[1,2]:"
echo "(1) New Instance, create ouput folder and folders"
echo "(2) Running Instance, save output to an existing folder"
read option
echo "............................"

echo "Location of input data files(Can contain one or more files):"
read input_data_folder
echo "............................"

while [ ! -d $input_data_folder ]
do
   echo Not a real directory, please input a real one:
   read input_data_folder
   echo ............................
done

if [ "$option" = "$answer3" ]
then
		echo New Directory where you want results, no slash at end:
		read output_folder
		echo ............................
		# Check to see if the directory is real.
		while [ ! -d $output_folder ]
		do
			echo Not a real directory, do you wish to create it? [Yes,No]
			read answer
		  if [ "$answer" = "$answer1" ]
		  then
		  	mkdir $output_folder
				mkdir $output_folder/Input_Data/
				mkdir $output_folder/Historical_Ratings/
				mkdir $output_folder/Historical_Ratings/Prioritize_Consistent/
				mkdir $output_folder/Historical_Ratings/Prioritize_New/
				mkdir $output_folder/Historical_Ratings/Seen_today_Only/
				mkdir $output_folder/Historical_Ratings/Traditional/
				touch $output_folder/Absolute_Data.csv
				touch $output_folder/Known_IPs.txt
				touch $output_folder/Processed_Splunk_Files.txt
				touch $output_folder/Times.csv
				touch $output_folder/Selected_modules.csv
				touch $output_folder/FP_log_file.csv
        			touch $output_folder/Aging-modifiers-pc.csv
        			touch $output_folder/Aging-modifiers-pn.csv
		  elif [ "$answer" = "$answer2" ]
		  then
		  	echo Input different location:
		  	read output_folder
				mkdir $output_folder/Historical_Ratings/
				mkdir $output_folder/Input_Data/
				mkdir $output_folder/Historical_Ratings/Prioritize_Consistent/
				mkdir $output_folder/Historical_Ratings/Prioritize_New/
				mkdir $output_folder/Historical_Ratings/Seen_today_Only/
				mkdir $output_folder/Historical_Ratings/Traditional/
				touch $output_folder/Absolute_Data.csv
				touch $output_folder/FP_log_file.csv
				touch $output_folder/Known_IPs.txt
				touch $output_folder/Processed_Splunk_Files.txt
				touch $output_folder/Times.csv
				touch $output_folder/Selected_modules.csv
		  else
		  	continue
			echo ............................
		  fi
		done
elif [ "$option" = "$answer4" ]
then
	echo "Please Input location of current instance ouput files:"
	read output_folder
fi

# Export all variables so they can be accessed by AIP.py
export output_folder
export input_data_folder

directory_of_AIP=$(dirname $(readlink -f "manual_run.sh"))

echo $directory_of_AIP
echo $directory_of_AIP/Main/Select_Modules.py

python3 $directory_of_AIP/Main/Select_Modules.py

for entry in $input_data_folder/*
do
   cp "$entry" $output_folder/Input_Data/
   echo "$entry"
   python3 $directory_of_AIP/Main/AIP.py
done
