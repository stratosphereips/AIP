import os
import csv

print("Hello World")

data_directory = os.environ['output_data_folder']

files = os.listdir(str(data_directory))

for file in files:
	with open(data_directory + file,'r') as f:
	    reader = csv.DictReader(f, delimiter=',')
	    rows = list(reader)
	    for row in rows:
	    	print(row['SrcAddr'])
	           
