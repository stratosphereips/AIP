# This script will be for changing the names of all the data files in Jin if we want.
import os

def find_new_data_files( directory_of_files):
    list_of_new_data_files = []
    list_of_data_files = os.listdir(directory_of_files)
    for file in list_of_data_files:
        if file not in list_of_processed_data_files:
            list_of_new_data_files.extend([file])
    for file12 in list_of_new_data_files:
        with open(c, 'a') as records_file1:
            records_file1.write(file12 + '\n')
    return list_of_new_data_files